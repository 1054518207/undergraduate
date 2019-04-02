"""
多进程爬虫
"""
import requests
from bs4 import BeautifulSoup
from random import choices
import multiprocessing as mp
import re
import os
import csv
import time
import random
import json
from mysql import connector
import uuid

local_proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}
proxy_url = "http://free-proxy-list.net/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

person = "/person.json"
affiliationGroups = "/affiliationGroups.json"
worksPage = "/worksPage.json?offset=0&sort=date&sortAsc=false"
pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\d')
dbname = "orcid"
dbuser = "root"
dbpassword = ""
infoTableName = "info"


def get_proxies(size=1):
    '''
    https代理查询，需要能科学上网，且打开ss
    :param size: 需要的代理数目
    :return: 字典型https代理
    '''
    time.sleep(random.random() * 5)
    flag = False
    while not flag:
        try:
            req = requests.get(proxy_url, headers=headers, proxies=local_proxies, timeout=10)
            flag = True
        except:
            print("网络超时……")
            pass
    soup = BeautifulSoup(req.content, "html.parser")
    all_tr = soup.find_all("tr")[1:]
    proxies_list = list()
    for item in all_tr:
        try:
            ip = item.find_all("td")[0].string
            port = item.find_all("td")[1].string
            https = item.find_all("td")[6].string
            if https == "yes":
                lt = list([ip, port])
                proxies_list.append(lt)
        except:
            break
    if len(proxies_list) >= size:
        return dict(choices(proxies_list, k=size))
    elif len(proxies_list) >= 1:
        return dict(choices(proxies_list, k=len(proxies_list)))


def test_crawl(start):
    proxy = get_proxies()
    for ip, port in proxy.items():
        print("{}使用代理为:{}:{}".format(mp.current_process().name, ip, port))
        break
    i = 0
    basetime = 0.5
    rows = 25
    writenum = 0
    cnt = 0
    name = mp.current_process().name
    # if not os.path.exists(name+".csv"):
    #     with open(name+".csv",'w',newline='') as csvfile:
    #         fieldnames = ['ORCIDiD', 'name', 'country', 'education', 'works']
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writeheader()

    # with open(name+".csv",'a+',newline='') as csvfile:
    #     fieldnames = ['ORCIDiD', 'name', 'country', 'education', 'works']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    print("{}进程第{}次尝试".format(name, i))
    url = "https://pub.sandbox.orcid.org/v2.1/search/?q=orcid&start={}&rows={}".format(start, rows)
    print(url)
    cnx = connector.connect(user=dbuser, database=dbname, password=dbpassword)
    cursor = cnx.cursor()
    add_info = (
            "INSERT INTO " + infoTableName +
            "(uuid,id,name,affiliationName,city,country,education) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)"
    )
    try:
        req = requests.Session()
        try:
            req = requests.get(url, proxies=proxy, headers=headers, timeout=10)
        except:
            print("进程{}无法获取xml信息".format(name))
        req.raise_for_status()
        if req.status_code == 200:
            req.encoding = "utf-8"
            text = req.text
            for uri in re.findall(pattern, text):
                if len(uri) == 45:
                    try:
                        # person.json
                        data = requests.get(uri + person, headers=headers, proxies=proxy, timeout=10)
                        time.sleep(basetime + random.random() * 1.2)
                        persondata = json.loads(data.text)
                        personname = persondata['displayName']
                        countryname = None
                        if persondata['countryNames'] is not None:
                            country = dict(persondata['countryNames'])
                            for key in country:
                                countryname = country[key]
                                break

                        # worksPage.json?offset=0&sort=date&sortAsc=false
                        # work = requests.get(uri+worksPage, headers=headers, proxies=proxy, timeout=10)
                        # time.sleep(basetime + random.random() * 1.2)
                        # workdata = json.loads(work.text)
                        # worknum = workdata['totalGroups']
                        # affiliationGroups.json
                        education = requests.get(uri + affiliationGroups, headers=headers, proxies=proxy, timeout=10)
                        time.sleep(basetime + random.random() * 1.2)
                        edudata = json.loads(education.text)
                        eduname = None
                        affiliationName = None
                        city = None
                        try:
                            eduname = edudata['affiliationGroups']['EDUCATION'][0]['affiliations'][0]['affiliationName']['value']
                        except:
                            pass
                        try:
                            affiliationName = edudata['affiliationGroups']['EMPLOYMENT'][
                                len(edudata['affiliationGroups']['EMPLOYMENT']) - 1]['affiliations'][0][
                                'affiliationName']['value']
                        except:
                            pass
                        try:
                            city = edudata['affiliationGroups']['EMPLOYMENT'][
                                len(edudata['affiliationGroups']['EMPLOYMENT']) - 1]['affiliations'][0]['city'][
                                'value']
                        except:
                            # print("未找到edu信息")
                            pass
                        # print("ORCIDiD:{};name:{},country:{},education:{},works:{}".format(uri,personname,countryname,eduname,worknum))
                        # writer.writerow({'ORCIDiD':uri,'name':personname,'country':countryname,'education':eduname,'works':worknum})
                        uid = uuid.uuid4()
                        add_value = [str(uid), uri, personname, affiliationName, city, countryname, eduname]
                        cursor.execute(add_info, add_value)
                        cnx.commit()
                        print("进程{}已成功写入{}次".format(name, writenum))
                        writenum += 1
                    except:
                        print("当前状态码：{}".format(data.status_code))
                        print("进程{}：url error {} times.".format(mp.current_process().name, cnt + 1))
                        cnt += 1
        else:
            print("网址相应错误")
    except:
        print("进程{}已执行{}次，中途错误，正在重新启动....".format(name, i))
        i -= 1
    finally:
        i += 1
    cursor.close()
    cnx.close()
    print("{}进程数据库写入完成".format(name))


def delete_duplicated_id(tbname=None):
    if tbname is None:
        raise RuntimeError("清除id错误，您未指定数据库名")
    cnx = connector.connect(user=dbuser, database=dbname, password=dbpassword)
    query = "SELECT id FROM " + tbname + " GROUP BY id HAVING COUNT(*) > 1"
    cursor = cnx.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    cnt = 1
    for item in records:
        id = item[0]
        sql = "SELECT uuid FROM " + tbname + " WHERE id = \"{}\"".format(id)
        cursor.execute(sql)
        data = cursor.fetchall()
        uid = data[0][0]
        delete_sql = "DELETE FROM " + tbname + " WHERE id = \"{}\" AND uuid != \"{}\"".format(id, uid)
        cursor.execute(delete_sql)
        print("已执行{}次".format(cnt))
        cnt += 1
    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    size = mp.cpu_count()
    start = [x for x in range(3, 10)]
    cnt = 0
    for ind in start:
        p1 = mp.Process(target=test_crawl, args=(ind * 100,), name="p1")
        p2 = mp.Process(target=test_crawl, args=(ind * 100 + 25,), name="p2")
        p3 = mp.Process(target=test_crawl, args=(ind * 100 + 50,), name="p3")
        p4 = mp.Process(target=test_crawl, args=(ind * 100 + 75,), name="p4")
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p1.terminate()
        p2.terminate()
        p3.terminate()
        p4.terminate()
