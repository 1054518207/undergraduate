import os
import requests
from PIL import Image, ImageEnhance
import numpy as np
import hashlib
import tensorflow as tf
from bs4 import BeautifulSoup

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"
}

login_url = "http://202.194.119.110/login.php"
verify_code_url = "http://202.194.119.110/vcode.php"
imgname = "code.png"
password = '1054518207a.'
user_id = '201558501224'
fromStuNum = "2017585011"
infoUrl = "http://202.194.119.110/ranklist.php?prefix="
totalNum = 60

# 验证码图片宽度
IMAGE_WIDTH = 60
# 验证码图片高度
IMAGE_HEIGHT = 24
# 存放训练好的模型的路径
MODEL_SAVE_PATH = './models/'
# 图片规格，10分类，一次4个
CHAR_SET_LEN = 10
CAPTCHA_LEN = 4


# 取得验证码图片的数据以及它的标签
def get_imgdata(fileName=None, Sess=None):
    if Sess is None:
        Sess = requests.Session()
    if fileName is None:
        raise RuntimeError("文件名不能为空")
    Sess.get(login_url, headers=headers)
    code = Sess.get(verify_code_url, headers=headers)
    with open(fileName, 'wb') as f:
        f.write(code.content)

    image = Image.open(fileName.format(os.getcwd()))
    imgry = image.convert('L')
    sharpness = ImageEnhance.Contrast(imgry)
    sharp_img = sharpness.enhance(2.0)
    # 转为灰度图
    image_array = np.array(sharp_img)
    image_data = image_array.flatten() / 255
    return image_data


# 构建卷积神经网络并训练
def validate_data_with_CNN(image_data=None):
    if image_data is None:
        raise RuntimeError("图像流不能为空")

    # 初始化权值
    def weight_variable(shape, name='weight'):
        init = tf.truncated_normal(shape, stddev=0.1)
        var = tf.Variable(initial_value=init, name=name)
        return var

    # 初始化偏置
    def bias_variable(shape, name='bias'):
        init = tf.constant(0.1, shape=shape)
        var = tf.Variable(init, name=name)
        return var

    # 卷积
    def conv2d(x, W, name='conv2d'):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME', name=name)

    # 池化
    def max_pool_2X2(x, name='maxpool'):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name=name)

        # 输入层

    # 请注意 X 的 name，在测试model时会用到它
    X = tf.placeholder(tf.float32, [None, IMAGE_WIDTH * IMAGE_HEIGHT], name='data-input')
    Y = tf.placeholder(tf.float32, [None, CAPTCHA_LEN * CHAR_SET_LEN], name='label-input')
    x_input = tf.reshape(X, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1], name='x-input')
    # 第一层卷积
    W_conv1 = weight_variable([5, 5, 1, 32], 'W_conv1')
    B_conv1 = bias_variable([32], 'B_conv1')
    conv1 = tf.nn.relu(conv2d(x_input, W_conv1, 'conv1') + B_conv1)
    conv1 = max_pool_2X2(conv1, 'conv1-pool')
    # 第二层卷积
    W_conv2 = weight_variable([5, 5, 32, 64], 'W_conv2')
    B_conv2 = bias_variable([64], 'B_conv2')
    conv2 = tf.nn.relu(conv2d(conv1, W_conv2, 'conv2') + B_conv2)
    conv2 = max_pool_2X2(conv2, 'conv2-pool')
    # 第三层卷积
    W_conv3 = weight_variable([5, 5, 64, 64], 'W_conv3')
    B_conv3 = bias_variable([64], 'B_conv3')
    conv3 = tf.nn.relu(conv2d(conv2, W_conv3, 'conv3') + B_conv3)
    conv3 = max_pool_2X2(conv3, 'conv3-pool')
    # 全链接层
    # 每次池化后，图片的宽度和高度均缩小为原来的一半，进过上面的三次池化，宽度和高度均缩小8倍
    W_fc1 = weight_variable([8 * 3 * 64, 1024], 'W_fc1')
    B_fc1 = bias_variable([1024], 'B_fc1')
    fc1 = tf.reshape(conv3, [-1, W_fc1.get_shape().as_list()[0]])
    fc1 = tf.nn.relu(tf.add(tf.matmul(fc1, W_fc1), B_fc1))
    # 输出层
    W_fc2 = weight_variable([1024, CAPTCHA_LEN * CHAR_SET_LEN], 'W_fc2')
    B_fc2 = bias_variable([CAPTCHA_LEN * CHAR_SET_LEN], 'B_fc2')
    output = tf.add(tf.matmul(fc1, W_fc2), B_fc2, 'output')

    predict = tf.reshape(output, [-1, CAPTCHA_LEN, CHAR_SET_LEN], name='predict')
    predict_max_idx = tf.argmax(predict, axis=2, name='predict_max_idx')
    saver = tf.train.Saver()
    config = tf.ConfigProto(allow_soft_placement=True,
                            log_device_placement=True)
    config.gpu_options.per_process_gpu_memory_fraction = 0.6
    with tf.Session(config=config) as sess:
        sess.run(tf.global_variables_initializer())
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)  # 获取checkpoints对象
        if ckpt and ckpt.model_checkpoint_path:  ##判断ckpt是否为空，若不为空，才进行模型的加载，否则从头开始训练
            print("正在恢复参数.....")
            saver.restore(sess, ckpt.model_checkpoint_path)  # 恢复保存的神经网络结构，实现断点续训
            print("参数恢复完成!")
        else:
            raise RuntimeError("未找到checkpoint文件")
        image_data = image_data.reshape((-1, 1440))
        predict = sess.run(predict_max_idx, feed_dict={X: image_data})
        return predict


def trylogin(vcode, sess=None):
    if sess is None:
        raise RuntimeError("会话不能为None")
    md = hashlib.md5()
    md.update(password.encode())
    post_data = {
        'user_id': user_id,
        'password': md.hexdigest(),
        'submit': '',
        'vcode': vcode
    }
    req = sess.post(login_url, headers=headers, data=post_data)
    req.encoding = 'utf-8'
    return req.text


def get_stu_info(stuNum, sess):
    '''

    :param stuNum:
    :param sess: requests
    :return:
    '''
    url = infoUrl + stuNum
    content = sess.get(url, headers=headers)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, "html.parser")
    info = []
    try:
        solveNum = soup.find("tr", attrs={"class": "evenrow"}).find_all("td")[4].find("a").string
        submitNum = soup.find("tr", attrs={"class": "evenrow"}).find_all("td")[5].find("a").string
        rate = soup.find("tr", attrs={"class": "evenrow"}).find_all("td")[6].string.strip()
        duplicateRate = soup.find("tr", attrs={"class": "evenrow"}).find_all("td")[7].find("div").string
        solveNum = int(solveNum)
        submitNum = int(submitNum)
        rate = rate[:len(rate)-1]
        duplicateRate = duplicateRate[:len(duplicateRate)-1]
        rate = float(rate)*.01
        duplicateRate = float(duplicateRate)*.01
        info.append(stuNum)
        info.append(solveNum)
        info.append(submitNum)
        info.append(rate)
        info.append(duplicateRate)
        if solveNum >= 10:
            return info
        else:
            return None
    except:
        return None


def init(needLogin = False):
    '''
    获取所有信息
    :param needLogin: 是否需要登录
    :return: 返回 list 类型数组信息
    '''
# if __name__ == '__main__':
    S = requests.Session()
    # needLogin = False
    if needLogin:
        print("正在尝试登录....")
        res = ""
        while len(res) < 500:
            imgdata = get_imgdata(imgname, S)
            predict = validate_data_with_CNN(imgdata)
            predict = predict.flatten()
            strpre = ""
            for num in predict:
                strpre = strpre + str(num)
            res = trylogin(strpre, S)
            if len(res) > 500:
                print("登录成功")
        os.remove(imgname)
    allinfo = []
    realnum = 0
    for ind in range(1, totalNum):
        stunum = fromStuNum
        if ind < 10:
            stunum = stunum + "0" + str(ind)
        else:
            stunum = stunum + str(ind)
        info = get_stu_info(stunum, S)
        if info is None:
            break
        realnum += 1
        allinfo.append(info)
        # print("{}信息为：{}".format(stunum, info))
    # print(allinfo)
    # npdata = np.array(allinfo)
    return allinfo,realnum,fromStuNum
