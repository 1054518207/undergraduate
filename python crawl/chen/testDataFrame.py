# -*- coding: utf-8 -*-
"""

@Author: lushaoxiao
@Date: 2019/3/31
@IDE: PyCharm
"""
import pandas as pd
import os
import numpy as np
import newlogin as nl
from sklearn.svm import SVC
from sklearn import metrics

def get_excel(excelFileName=None):
    '''
    根据参数获取excel文件内容 eg: excelFileName = 175
    :param excelFileName: excel文件名称，若为None则为获取训练数据，非空为测试集
    :return: 文档名字
    '''
    baseDir = "D:/undergraduate/python crawl/chen/"
    all_files = os.listdir(baseDir)
    fileName = None
    if excelFileName is None:
        for item in all_files:
            if item.endswith("xlsx") and item.__contains__("171"):
                fileName = item
                break
        return fileName
    else:
        for item in all_files:
            if item.endswith("xlsx") and item.__contains__(str(excelFileName)):
                fileName = item
                break
        if fileName is None:
            raise RuntimeError("Can't find {} document".format(excelFileName))
        # print(baseDir + fileName)
        return baseDir + fileName

def get_label(excelFileName = None, allStuInfo = None):
    '''
    根据excel文件，返回加标签的DataFrame对象
    :param excelFileName: excel文档名，可以为None
    :param allStuInfo: 所有学生信息，列表形式
    :return: 带标签的DataFrame对象
    '''
    if allStuInfo is None:
        raise RuntimeError("学生信息不能为空，否则无法获取学生等级标签")
    df = pd.read_excel(get_excel(excelFileName), skiprows=2, dtype=str)
    df = df[['User', 'Nick', 'Solved']]
    dfCrawlData = pd.DataFrame(allStuInfo, columns=['User', 'Accept', 'Submit', 'Rate', 'DuplicatedRate'], dtype=str)
    # 双表去重,一个根据excel,一个根据数据信息
    df = df[df['User'].isin(dfCrawlData['User'])]
    dfCrawlData = dfCrawlData[dfCrawlData['User'].isin(df['User'])]
    df.index = [x for x in range(0, len(df))]
    dfCrawlData.index = [x for x in range(0, len(dfCrawlData))]
    df = df.merge(dfCrawlData, left_on='User', right_on='User')
    maxnum = pd.DataFrame.max(df['Solved'].astype(float))
    level = []
    for x in df['Solved']:
        if float(x) >= int(0.75 * maxnum):
            level.append('A')
        elif float(x) >= int(0.2 * maxnum):
            level.append('B')
        else:
            level.append('D')
    df.loc[:, 'level'] = level
    return df

if __name__ == '__main__':
    crawlData = [['201758501101', 160, 374, 0.42781, 0.6038], ['201758501102', 189, 721, 0.26214, 0.5271], ['201758501103', 170, 503, 0.33797, 0.765], ['201758501104', 80, 198, 0.40404000000000007, 0.7775], ['201758501105', 169, 681, 0.24816, 0.6443000000000001], ['201758501106', 130, 253, 0.51383, 0.856], ['201758501107', 160, 521, 0.30710000000000004, 0.8417], ['201758501108', 175, 337, 0.51929, 0.5189], ['201758501109', 224, 570, 0.39298000000000005, 0.4975], ['201758501110', 186, 480, 0.3875, 0.644], ['201758501111', 264, 550, 0.48, 0.45280000000000004], ['201758501112', 289, 692, 0.41763, 0.34880000000000005], ['201758501113', 170, 370, 0.45946, 0.7272], ['201758501114', 350, 809, 0.43263, 0.41990000000000005], ['201758501115', 198, 486, 0.40741, 0.6357], ['201758501116', 186, 547, 0.34004, 0.5552], ['201758501117', 206, 528, 0.39015, 0.6009000000000001], ['201758501118', 164, 398, 0.41206000000000004, 0.7062], ['201758501119', 214, 473, 0.45243000000000005, 0.7088], ['201758501120', 193, 550, 0.35091, 0.5902000000000001], ['201758501121', 404, 894, 0.45189999999999997, 0.36479999999999996], ['201758501122', 214, 616, 0.34740000000000004, 0.6458], ['201758501123', 186, 467, 0.39829000000000003, 0.6888], ['201758501124', 249, 682, 0.3651, 0.4182], ['201758501125', 202, 465, 0.43441, 0.52], ['201758501126', 274, 675, 0.40593000000000007, 0.5049], ['201758501127', 173, 569, 0.30404000000000003, 0.7156999999999999], ['201758501128', 182, 379, 0.48021, 0.6269], ['201758501129', 162, 337, 0.48070999999999997, 0.44439999999999996], ['201758501130', 197, 511, 0.38552000000000003, 0.6618], ['201758501131', 202, 485, 0.41649, 0.5234000000000001], ['201758501132', 275, 1158, 0.23748000000000002, 0.594], ['201758501133', 185, 380, 0.48684, 0.5975], ['201758501134', 249, 531, 0.46893, 0.43590000000000007], ['201758501135', 174, 363, 0.47934, 0.7003], ['201758501136', 199, 530, 0.37546999999999997, 0.5626], ['201758501137', 203, 480, 0.42292, 0.6967], ['201758501138', 167, 352, 0.47442999999999996, 0.7434000000000001], ['201758501139', 144, 459, 0.31373, 0.6282], ['201758501140', 200, 380, 0.52632, 0.6267], ['201758501141', 182, 375, 0.48533000000000004, 0.7112999999999999], ['201758501142', 199, 563, 0.35346, 0.47659999999999997], ['201758501143', 190, 468, 0.40598, 0.7186], ['201758501144', 194, 442, 0.43890999999999997, 0.7491], ['201758501145', 262, 648, 0.40432, 0.5173], ['201758501146', 188, 516, 0.36434, 0.7879], ['201758501147', 201, 443, 0.45372, 0.7397], ['201758501148', 193, 463, 0.41685000000000005, 0.7170000000000001], ['201758501149', 209, 542, 0.38561, 0.7148000000000001], ['201758501150', 127, 492, 0.25812999999999997, 0.6904000000000001], ['201758501151', 188, 421, 0.44656, 0.7202], ['201758501152', 171, 478, 0.35774, 0.7352]]

    # print("Initial information ……")

    # crawlData,realNum = nl.init(needLogin=False, custome=False)
    df = get_label("171",crawlData)

    # print("Inital successfully,start create model……")

    clf = SVC(kernel="linear", C=100)
    data_in = df[['Accept','Submit','Rate','DuplicatedRate']].astype(np.float)
    data_lable = df['level'].astype(str)
    clf.fit(np.array(data_in),np.array(data_lable))

    # print("Model build successfully,start predict……")

    testCrawlData, realNum = nl.init(needLogin=False,custome=True,stuNum="2017585051")
    dfTest = get_label("175",testCrawlData)
    data_in = dfTest[['Accept', 'Submit', 'Rate', 'DuplicatedRate']].astype(np.float)
    # test_data = np.array([[345,1112,.31025,.4007],[225,824,.27306,.6936],[307,960,.31979,.5012],[104,254,.40945,.7294]],dtype=np.float)
    predictLabel = clf.predict(data_in)
    trueLabel = dfTest['level']

    # print("Accuracy:{}".format(metrics.accuracy_score(trueLabel,predictLabel)))

    dfPredict = pd.DataFrame(data={"num":dfTest['User'],"trueLabel":dfTest['level'],
                                   "predictLabel":predictLabel})
    pd.set_option("display.max_info_rows",100)
    # print(dfPredict)

    print(dfPredict['num'].to_json())
    print(dfPredict['predictLabel'].to_json())
