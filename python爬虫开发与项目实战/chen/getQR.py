import requests
import os

url = "http://202.194.119.110/vcode.php"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

pathname = os.getcwd() + "/pictttt"
if not os.path.exists(pathname):
    os.mkdir(pathname)
if os.path.exists(pathname):
    os.chdir(pathname)
    for i in range(100):
        req = requests.get(url, headers=header)
        with open(str(i)+'.png','wb') as f:
            f.write(req.content)
            print("已爬取{}次。".format(i+1))
        # break