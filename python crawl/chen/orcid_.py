import requests
from bs4 import BeautifulSoup
import json
from pandas import DataFrame
import time

session=requests.session()
# 'Cookie': 'X-Mapping-fjhppofk=44B27ECF9D6192E10AC06F4274772E24; XSRF-TOKEN=1651ff5d-c188-4018-a6f0-5daa663f2da3; JSESSIONID=1959865153011C6EBF8924E8C94A920B; _gid=GA1.2.288754350.1553413224; _ga=GA1.2.252667569.1553413224; __cfduid=d4b84dd19dc9ec7b833a2f32d5e87100c1553413222'}

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
}
id_urls = []
info_all = []
aff_all = []
work_all = []
work_key = ['eid', 'doi']
for start in range(25):
    url = "https://pub.orcid.org/v2.1/search/?q=%7B!edismax%20qf%3D%22given-and-family-names%5E50.0%20family-name%5E10.0%20given-names%5E5.0%20credit-name%5E10.0%20other-names%5E5.0%20text%5E1.0%22%20pf%3D%22given-and-family-names%5E50.0%22%20mm%3D1%7Dundefined&start={}&rows=10".format(
        start)
    r = session.get(url, headers=head)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    l = [x.text for x in soup.find_all('common:uri')]
    id_urls.extend(l)
# print('url_id:',id_urls)
for id_url in id_urls:
    person_url = id_url + '/person.json'
    affiliationGroups_url = id_url + '/affiliationGroups.json'
    work_url = id_url + "/worksPage.json?offset=0&sort=date&sortAsc=false"

    print("person_url:", person_url)
    print("aff_url:", affiliationGroups_url)
    print("work_url:", work_url)

    '''对person.json发出请求'''
    r_person = session.get(person_url, headers=head)
    person_dict = json.loads(r_person.text)
    # print(person_dict)
    displayName = person_dict['displayName']
    # print(person_dict['countryNames'])
    if person_dict['countryNames'] != {} and person_dict['countryNames'] is not None:
        countryNames = "".join(person_dict['countryNames'].values())
    else:
        countryNames = " "
    if person_dict['publicGroupedKeywords'] == {} or person_dict['publicGroupedKeywords'] == None:
        publicGroupedKeywords = " "
    else:
        publicGroupedKeywords = person_dict['publicGroupedKeywords']
    info = [id_url[-19:], displayName, countryNames, publicGroupedKeywords]
    info_all.append(info)
    print("info",info)

    '''对affiliationGroup_url发出请求'''
    r_aff = session.get(affiliationGroups_url, headers=head)
    #print(r_aff.text)
    aff_dict = json.loads(r_aff.text)
    if len(aff_dict['affiliationGroups']['EMPLOYMENT']) == 0 or aff_dict['affiliationGroups']['EMPLOYMENT'] == None:
        aff_all.append([" " for x in range(8)])
    else:
        for l in aff_dict['affiliationGroups']['EMPLOYMENT']:
            time.sleep(1)
            l = l['defaultAffiliation']
            affiliationName = l['affiliationName']['value']
            city = l['city']['value']
            region = l['region']['value']
            dateSortString = l['dateSortString']
            departmentName = l['departmentName']['value']
            source = l['sourceName']
            aff_all.append(
                [id_url[-19:], displayName, affiliationName, city, region, dateSortString, departmentName, source])
            # print(l['affiliationName']['value'],l['city']['value'],l['region']['value'],l['dateSortString'],l['departmentName']['value'],l['sourceName'])
    print('aff:',aff_all)
    '''对work_url发出请求'''
    r_work = session.get(work_url, headers=head)
    work_dict = json.loads(r_work.text)['groups']
    for Y in work_dict:
        time.sleep(1)
        doi_eid = {'doi': "", 'eid': ""}
        work = Y['works'][0]
        title = work['title']['value']
        if work['journalTitle'] != {} and work['journalTitle'] is not None:
            journaTitle = work['journalTitle']['value']
        else:
            journaTitle = " "
        if work['publicationDate'] != {} and work['publicationDate'] is not None:
            publicationDate = work['publicationDate']['year']
        else:
            publicationDate = " "
        #publicationDate = work['publicationDate']['year']
        workType = work['workType']['value']
        for w in work['workExternalIdentifiers']:
            t = w['externalIdentifierType']['value']
            doi_eid[t] = w['externalIdentifierId']['value']
        #         DOI=work['workExternalIdentifiers'][0]['normalized']['value']
        #         #EID=work['workExternalIdentifiers'][1]['normalized']['value']
        #         if len(Y['externalIdentifiers'])>1:
        #             EID=Y['externalIdentifiers'][1]['externalIdentifierId']['value']
        #         else:
        #             EID=' '
        work_all.append([id_url[-19:], displayName, title, journaTitle, publicationDate, workType, doi_eid['doi'], doi_eid['eid']])
    # print('work:',work_all)

info = {'ORCID': [ORCID[0] for ORCID in info_all],
        'NAME': [ORCID[1] for ORCID in info_all],
        'conntry': [ORCID[2] for ORCID in info_all],
        'keywords': [ORCID[3] for ORCID in info_all],
        }
frame_info = DataFrame(info)
# 导出到excel文件
frame_info.to_csv('person_info.csv', index=True, encoding="utf-8")

affiliationGroups = {'ORCID': [aff[0] for aff in aff_all],
                     'NAME': [aff[1] for aff in aff_all],
                     'affiliationName': [aff[2] for aff in aff_all],
                     'city': [aff[3] for aff in aff_all],
                     'region': [aff[4] for aff in aff_all],
                     'present_date': [aff[5] for aff in aff_all],
                     'department': [aff[6] for aff in aff_all],
                     'source': [aff[7] for aff in aff_all], }
frame_aff = DataFrame(affiliationGroups)
frame_aff.to_csv("affiliationGroups.csv", index=True, encoding="utf-8")

works = {"ORCID": [work[0] for work in work_all],
         'NAME': [work[1] for work in work_all],
         'title': [work[2] for work in work_all],
         'JournaTitle': [work[3] for work in work_all],
         'publictation': [work[4] for work in work_all],
         'workType': [work[5] for work in work_all],
         'DOI': [work[6] for work in work_all],
         'EID': [work[7] for work in work_all]}
frame_work = DataFrame(works)
frame_work.to_csv('work.csv', index=True, encoding="utf-8")
