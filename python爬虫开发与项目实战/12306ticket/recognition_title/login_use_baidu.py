"""
 利用百度图像识别api做文字识别，目的是为了做12306的图片校验。
"""
from aip import AipOcr

# 定义常量
APP_ID = '10836850'
API_KEY = 'VAgKccmIuGdxSdGzewCwCFc8'
SECRET_KEY = 'MVtU0Mpb8zdDSbEd3GrWIhDFKYNH2s6y'

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

class BaiDu(object):
    # 获取图片
    def get_file_content(self, file_path):
        '''
        获取图片数据
        :param file_path: 图片路径 
        :return: 图片信息
        '''
        with open(file_path, 'rb') as f:
            return f.read()

    def get_result(self, image_url):
        '''
        识别结构
        :param image_url: 图片存储路径
        :return: 返回识别结果
        '''
        image = self.get_file_content(image_url)
        return client.basicGeneral(image, options)

if __name__ == '__main__':
    #获取图片
    baidu = BaiDu()
    result = baidu.get_result("../images/double.png")
    print(result['words_result'][0]['words'])
