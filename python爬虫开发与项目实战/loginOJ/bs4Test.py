import requests
from bs4 import BeautifulSoup

S = requests.session()
req = S.get("http://202.194.119.110/contest.php?cid=4444")
req.encoding = 'utf-8'
soup = BeautifulSoup(req.text, "html.parser")
if soup.find('input'):
    print("你没有进入该测试的条件")
elif soup.find('title').string == u'比赛已经关闭!':
    print("输入测试号码错误")
else:
    print("ok")

req = S.get("http://202.194.119.110/status.php?user_id=201558501224&cid=1884")
req.encoding = 'utf-8'
soup = BeautifulSoup(req.text, "html.parser")
for tr in soup.find('tbody').children:
    import bs4
    if isinstance(tr, bs4.element.Tag):
        tds = tr.find_all("td")
        print(tds)
text = soup.find('span', attrs={"class":"btn"}).string
print(text)
text = soup.select('.btn')[1].string
print(text)