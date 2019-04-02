import os
import re
import requests
from PIL import Image, ImageEnhance
from pytesseract import pytesseract
from bs4 import BeautifulSoup

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"
}

login_url = "http://202.194.119.110/login.php"
verify_code_url = "http://202.194.119.110/vcode.php"

S = requests.Session()
S.get(login_url, headers=headers)
code = S.get(verify_code_url, headers=headers)
with open("code.gif", 'wb') as f:
    f.write(code.content)

image = Image.open('{}/code.gif'.format(os.getcwd()))
imgry = image.convert('L')
sharpness = ImageEnhance.Contrast(imgry)
sharp_img = sharpness.enhance(2.0)
sharp_img.save("{}/code1.gif".format(os.getcwd()))
pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"
verify_code = pytesseract.image_to_string(Image.open('./code1.gif'))
verify_code = re.findall("\d+", verify_code.strip())
post_data = {
    'password': '1054518207a.',
    'submit': 'Submit',
    'user_id': '201558501224',
    'vcode': verify_code
}
print(verify_code)
req = S.post(login_url, headers=headers, data=post_data)
req.encoding = 'utf-8'
print(req.text)
if '-2' in req.text:
    print("登录成功")
else:
    print("登录失败")
# soup = BeautifulSoup(req.text, "html.parser")

