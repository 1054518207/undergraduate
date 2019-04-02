import requests
import multiprocessing as mp
import re
import os
import csv
import time
import random
import json
from bs4 import BeautifulSoup
from random import choices

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

def get_proxies(size=1):
    '''
    https代理查询，需要能科学上网，且打开ss
    :param size: 需要的代理数目
    :return: 字典型https代理
    '''
    try:
        req = requests.get(proxy_url, headers=headers, proxies=local_proxies, timeout=10)
    except:
        raise RuntimeError("网络超时……")
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
    else:
        return None

def test_crawl(start,proxy):
    i = 0
    basetime = 0.5
    rows = int(100 / mp.cpu_count())
    maxtimes = int(100 / rows)
    writenum = 0
    cnt = 0
    name = mp.current_process().name
    if not os.path.exists(name+".csv"):
        with open(name+".csv",'w',newline='') as csvfile:
            fieldnames = ['ORCIDiD', 'name', 'country', 'education', 'works']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(name+".csv",'a+',newline='') as csvfile:
        fieldnames = ['ORCIDiD', 'name', 'country', 'education', 'works']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        while i < maxtimes:
            print("{}进程第{}次尝试".format(name,i))
            url = "https://pub.sandbox.orcid.org/v2.1/search/?q=orcid&start={}&rows={}".format(start,rows)
            print(url)
            try:
                req = requests.Session()
                try:
                    req = requests.get(url,proxies=proxy,headers=headers,timeout=10)
                except:
                    print("进程{}无法获取xml信息".format(name))
                req.raise_for_status()
                if req.status_code == 200:
                    req.encoding = "utf-8"
                    text = req.text
                    for uri in re.findall(pattern, text):
                        if len(uri) == 45:
                            try:
                                data = requests.get(uri+person, headers=headers, proxies=proxy, timeout=10)
                                time.sleep(basetime + random.random() * 1.2)
                                persondata = json.loads(data.text)
                                personname = persondata['displayName']
                                countryname = ""
                                if persondata['countryNames'] is not None:
                                    country = dict(persondata['countryNames'])
                                    for key in country:
                                        countryname = country[key]
                                        break
                                work = requests.get(uri+worksPage, headers=headers, proxies=proxy, timeout=10)
                                time.sleep(basetime + random.random() * 1.2)
                                workdata = json.loads(work.text)
                                worknum = workdata['totalGroups']
                                education = requests.get(uri+affiliationGroups, headers=headers, proxies=proxy, timeout=10)
                                time.sleep(basetime + random.random() * 1.2)
                                edudata = json.loads(education.text)
                                eduname = ""
                                try:
                                    eduname = edudata['affiliationGroups']['EDUCATION'][0]['affiliations'][0]['affiliationName']['value']
                                except:
                                    # print("未找到edu信息")
                                    pass
                                # print("ORCIDiD:{};name:{},country:{},education:{},works:{}".format(uri,personname,countryname,eduname,worknum))
                                writer.writerow({'ORCIDiD':uri,'name':personname,'country':countryname,'education':eduname,'works':worknum})
                                print("进程{}已成功写入{}次".format(name,writenum))
                                writenum += 1
                            except:
                                print("当前状态码：{}".format(data.status_code))
                                print("url error {} times.".format(cnt))
                                cnt += 1
                else:
                    print("网址相应错误")
            except:
                print("进程{}已执行{}次，中途错误，正在重新启动....".format(name,i))
                i -= 1
            finally:
                i += 1

if __name__ == '__main__':
    size = mp.cpu_count()
    # proxy_dic = get_proxies(size=size)
    proxy1 = {
        "5.160.39.226":"52550",
        "54.36.44.250": "8080"
    }
    proxy2 = {
        "54.36.44.250": "8080"
    }
    p1 = mp.Process(target=test_crawl, args=(0,proxy1,))
    p2 = mp.Process(target=test_crawl, args=(0, proxy2,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    # url = "https://sandbox.orcid.org/0000-0001-6334-5944"
    # req = requests.get(url+person,headers=headers,proxies=proxy)
    # req.encoding = "utf-8"
    # print(req.text)
    # ll = list(item for item in proxy1.items())
    # print("{}:{}".format(ll[0][0],ll[0][1]))
