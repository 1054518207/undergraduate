import os
import re
import requests
import time
from PIL import Image, ImageEnhance
from pytesseract import pytesseract
from bs4 import BeautifulSoup

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"
}

login_url = "http://202.194.119.110/login.php"
verify_code_url = "http://202.194.119.110/vcode.php"
start_url = "http://202.194.119.110/loginpage.php"

# pytesseract执行路径，以及预测数据路径
pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"

class YTUojlogin():
    def __init__(self):
        self.login_url = login_url
        self.verify_code_url = verify_code_url
        self.start_url = start_url
        self.headers = headers
        self.S = requests.session()
        self.username = ''
        self.password = ''
        self.error = 0

    def get_start(self):
        try:
            self.S.get(self.start_url, headers=self.headers)
            print("请输入用户名：", end='')
            self.username = input()
            print("请输入密码：", end='')
            self.password = input()
            print("正在登录，请稍后.....")
        except:
            print("网络异常或者服务器崩溃")
            exit(-1)
        while not self.get_code():
            pass

    def get_code(self):
        '''
        
        :return: code image
        '''
        code = self.S.get(verify_code_url, headers=self.headers)
        with open("code.gif", 'wb') as f:
            f.write(code.content)

        # 将图片二值化，增大对比度提高识别成功概率
        image = Image.open('{}/code.gif'.format(os.getcwd()))
        imgry = image.convert('L')
        sharpness = ImageEnhance.Contrast(imgry)
        sharp_img = sharpness.enhance(2.0)
        sharp_img.save("{}/code1.gif".format(os.getcwd()))

        # 开始对图片进行识别
        verify_code = pytesseract.image_to_string(Image.open('./code1.gif'))
        verify_code = re.findall("\d+", verify_code.strip())

        # post_data
        post_data = {
            'password': self.password,
            'submit': 'Submit',
            'user_id': self.username,
            'vcode': verify_code
        }

        req = self.S.post(login_url, headers=headers, data=post_data)
        req.encoding = 'utf-8'
        # print(req.text)
        if '-2' in req.text:
            print("登录成功")
            return True
        elif re.search(r"(?<=U).*?(?=e)", req.text):
            print("用户名或者密码错误")
            self.set_error()
            return True
        else:
            # print("登录失败")
            return False

    def set_error(self):
        self.error = 1

    def get_error(self):
        if self.error:
            return True
        else:
            return False

    def change_contest(self):
        contest_post_url = "http://202.194.119.110/submit.php"
        print("输入竞赛号：", end='')
        conum = input()
        req = self.S.get("http://202.194.119.110/contest.php?cid={}".format(conum), headers=headers)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, "html.parser")
        if soup.find('input'):
            print("你没有进入该竞赛的条件")
            exit(-3)
        elif soup.find('title').string == u'比赛已经关闭!':
            print("输入竞赛号码错误")
            exit(-4)
        print("输入题号：", end='')
        pronum = input()
        f = open('source.c', 'r')
        source = f.read()
        f.close()
        # print(source)
        ppost = {
            'cid': conum,
            'language': '0',
            'pid': pronum,
            'reverse2': 'reverse',
            'source': source
        }
        self.S.post(contest_post_url, headers=headers, data=ppost)
        flag = True
        print("提交成功，编译中......")
        time.sleep(2)
        while flag:
            req = self.S.get("http://202.194.119.110/status.php?user_id={}&cid={}".format(self.username, conum), headers=headers)
            req.encoding = 'utf-8'
            soup = BeautifulSoup(req.text, "html.parser")
            text = soup.select('.btn')[1].string
            # print(text)
            if not (text == 'Pending' or text == 'Compiling' or text == 'Running & Judging'):
                flag = False
                print(text)
            else:
                time.sleep(1)

if __name__ == '__main__':
    log = YTUojlogin()
    log.get_start()
    os.remove("{}/code.gif".format(os.getcwd()))
    os.remove("{}/code1.gif".format(os.getcwd()))
    if log.get_error():
        exit(-2)
    log.change_contest()
