import requests
import re
import json
import csv
import time
import random

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}

req = requests.session()
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    # "cookie": "__cfduid=d95df65dc2e5c3060d55ecb448541430d1553487966; X-Mapping-fjhppofk=44B27ECF9D6192E10AC06F4274772E24; _ga=GA1.2.1343885275.1553487965; _gid=GA1.2.1748701278.1553487965; orcidCookiePolicyAlert=dont%20show%20message; locale_v3=zh_CN; XSRF-TOKEN=f9552881-4514-434e-ae24-9971ade3a7e8; JSESSIONID=AE2495F2AC45248757FF3B4638572D4B; has_js=1"
}

# url = "https://orcid.org/0000-0002-7847-5431"
cnt = 1
writenum = 1
start = [x for x in range(100)]
person = "/person.json"
affiliationGroups = "/affiliationGroups.json"
worksPage = "/worksPage.json?offset=0&sort=date&sortAsc=false"
pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\d')

# with open("info.csv",'w',newline='') as csvfile:
#     fieldnames = ['ORCIDiD', 'name', 'country', 'education', 'works']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

tt = 0
maxtimes = 2000
i = 0
basetime = 0.5

while tt <= maxtimes:
    with open("info.csv",'a+',newline='') as csvfile:
        fieldnames = ['ORCIDiD', 'name', 'country', 'education', 'works']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        while i <= maxtimes:
            print("{}次尝试".format(i))
            url = "https://pub.sandbox.orcid.org/v2.1/search/?q=orcid&start={}&rows=10".format(i*10)
            try:
                htmlcontent = None
                try:
                    htmlcontent = req.get(url, headers=header, proxies=proxies, timeout=10)
                except:
                    print("无法获取xml信息")
                htmlcontent.raise_for_status()
                if htmlcontent.status_code == 200:
                    htmlcontent.encoding = htmlcontent.apparent_encoding
                    text = htmlcontent.text
                    for uri in re.findall(pattern, text):
                        if len(uri) == 45:
                            try:
                                data = req.get(uri+person, headers=header, proxies=proxies, timeout=10)
                                time.sleep(basetime + random.random() * 1.2)
                                persondata = json.loads(data.text)
                                personname = persondata['displayName']
                                countryname = ""
                                if persondata['countryNames'] is not None:
                                    country = dict(persondata['countryNames'])
                                    for key in country:
                                        countryname = country[key]
                                        break
                                work = req.get(uri+worksPage, headers=header, proxies=proxies, timeout=10)
                                time.sleep(basetime + random.random() * 1.2)
                                workdata = json.loads(work.text)
                                worknum = workdata['totalGroups']
                                education = req.get(uri+affiliationGroups, headers=header, proxies=proxies, timeout=10)
                                time.sleep(basetime + random.random() * 1.2)
                                edudata = json.loads(education.text)
                                eduname = ""
                                try:
                                    eduname = edudata['affiliationGroups']['EDUCATION'][0]['affiliations'][0]['affiliationName']['value']
                                except:
                                    print("未找到edu信息")
                                    pass
                                # print("ORCIDiD:{};name:{},country:{},education:{},works:{}".format(uri,personname,countryname,eduname,worknum))
                                writer.writerow({'ORCIDiD':uri,'name':personname,'country':countryname,'education':eduname,'works':worknum})
                                print("已成功写入{}次".format(writenum))
                                writenum += 1
                            except:
                                print("当前状态码：{}".format(data.status_code))
                                print("url error {} times.".format(cnt))
                                cnt += 1
                else:
                    print("网址相应错误")
            except:
                print("已执行{}次，中途错误，正在重新启动....".format(i))
                i += 1
                tt = i
            i += 1
