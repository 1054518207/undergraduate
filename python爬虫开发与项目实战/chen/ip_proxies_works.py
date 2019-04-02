# -*- coding: utf-8 -*-
"""
四进程爬虫，爬取orcid网址的信息，转存至works表
@Author: lushaoxiao
@Date: 2019/3/31
@IDE: PyCharm
"""
import requests
import json
from mysql import connector
import ip_proxies
import multiprocessing as mp
import uuid

# 获取works信息json数据链接
workurl = "/worksPage.json?offset=0&sort=date&sortAsc=false"
# 论文地址前链接
basePaperUrl = "https://doi.org/"
# 数据库设置
dbuser = "root"
dbpassword = ""
dbname = "orcid"
infoTableName = "info"
tableName = "works"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

def get_work_info(urls):
    '''
    获取works json数据信息
    :param urls: works信息url列表
    :return:
    '''
    cnx = connector.connect(user=dbuser, database=dbname, password=dbpassword)
    insert_query = (
            "INSERT INTO " + tableName +
            "(uuid,id,title,journal_title,year,month,day,work_type,paper_url)" +
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    cursor = cnx.cursor()
    cnt = 0
    # 获取代理
    proxy = None
    while proxy is None:
        proxy = ip_proxies.get_proxies()
    ip = None
    port = None
    for i,p in proxy.items():
        ip = i
        port = p
        break
    print("{}进程获取代理成功，代理ip：{}；代理端口：{}".format(mp.current_process().name,ip,port))
    for url in urls:
        ff = True
        get_cnt = 1
        """
            获取works网址信息，出错原因：
            1.当前网络问题，尝试获取3次
            2.当前代理出错，尝试换一个IP代理
        """
        while ff and get_cnt <= 3:
            try:
                req = requests.get(url=url + workurl, headers=headers, proxies=proxy, timeout=5)
                ff = False
                # print("{}进程需要获取url为：{}".format(mp.current_process().name,url+workurl))
            except:
                print("进程{}获取works信息失败，正在重试".format(mp.current_process().name))
                get_cnt += 1
        if get_cnt > 3:
            # 获取信息失败，尝试重新获取代理（可能代理出错）
            proxy = None
            while proxy is None:
                proxy = ip_proxies.get_proxies()
            continue
        # 获取成功，开始解析json
        jsondata = json.loads(req.content)
        groups = jsondata['groups']
        for item in groups:
            title = item['works'][0]['title']['value']
            if title is None:
                continue
            journalTitle = None
            year = None
            month = None
            day = None
            workType =None
            paperurl = None
            try:
                journalTitle = item['works'][0]['journalTitle']['value']
            except:
                pass
            try:
                year = item['works'][0]['publicationDate']['year']
                month = item['works'][0]['publicationDate']['month']
                day = item['works'][0]['publicationDate']['day']
            except:
                pass
            try:
                workType = item['works'][0]['workType']['value']
            except:
                pass
            try:
                tmpurl = str(item['externalIdentifiers'][0]['externalIdentifierId']['value'])
                if tmpurl.startswith("http"):
                    paperurl = tmpurl
                else:
                    paperurl = basePaperUrl + tmpurl
            except:
                pass
            uid = str(uuid.uuid4())
            datainfo = [uid,url,title,journalTitle,year,month,day,workType,paperurl]
            cursor.execute(insert_query,datainfo)
            cnx.commit()
            # print("{}进程已写入{}次。".format(mp.current_process().name,cnt))
            # cnt += 1
            # print(title)
            # print(journalTitle)
            # print("{}-{}-{}|{}".format(year,month,day,workType))
            # print("paperurl:{}".format(paperurl))
            # print("*****************")
        cnt += 1
    print("{}进程写入完成{}次。".format(mp.current_process().name, cnt))
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    # 开始从数据库获取所有url信息，转换为列表
    cnx = connector.connect(user=dbuser, database=dbname, password=dbpassword)
    query = "SELECT id FROM " + infoTableName
    cursor = cnx.cursor()
    cursor.execute(query)
    lt = cursor.fetchall()
    cursor.close()
    cnx.close()
    # 所有url计数
    totalnum = len(lt)
    cnt = 0
    # 一次主进程完成需要爬取的url总数
    base = 100
    # 一个进程需要爬取的url链接数
    onecount = 25
    # 清洗数据库查询的列表，自己查看lt列表内容就能明白
    records = []
    for x in lt:
        records.append(x[0])
    # 爬取所有url
    while cnt < int(totalnum/base):
        # 四进程并发执行
        p1 = mp.Process(target=get_work_info, args=(records[cnt * base + 0 :cnt * base + onecount + 0],), name="p1")
        p2 = mp.Process(target=get_work_info, args=(records[cnt * base + 25:cnt * base + onecount + 25],), name="p2")
        p3 = mp.Process(target=get_work_info, args=(records[cnt * base + 50:cnt * base + onecount + 50],), name="p3")
        p4 = mp.Process(target=get_work_info, args=(records[cnt * base + 75:cnt * base + onecount + 75],), name="p4")
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
        cnt += 1
        print("主进程已完成{}次。".format(cnt))
