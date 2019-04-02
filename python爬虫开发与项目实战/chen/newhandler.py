import newlogin as nl
import numpy as np
from sklearn.svm import SVC
import pandas as pd
import os
import warnings

def get_excel():
    all_files = os.listdir(".")
    filename = None
    for item in all_files:
        if item.endswith("xlsx"):
            filename = item
    return filename

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    excel_name = get_excel()
    pddata = None
    if excel_name is not None:
        try:
            pddata = pd.read_excel(excel_name,skiprows=2,dtype=str)
        except:
            raise RuntimeError("excel文件错误")
    else:
        raise RuntimeError("未找到excel文件")
    fpddata = pddata[['User','Nick','Solved']]
    lt = []
    for x in fpddata['User']:
        lt.append(x)
    maxnum = pd.DataFrame.max(pddata['Solved'].astype(float))
    level = []
    for x in fpddata['Solved']:
        if float(x) >= int(0.75*maxnum):
            level.append('A')
        elif float(x) >= int(0.2*maxnum):
            level.append('B')
        else:
            level.append('D')
    allinfo,realnum,fromStuNum = nl.init(needLogin=False)
    df = pd.DataFrame(allinfo,columns=['User','Accept','Submit','Rate','DuplicatedRate'],dtype=str)
    # fpddata['level'] = level
    fpddata.loc[:,'level'] = level
    pd.set_option('display.max_columns',10)
    # 根据班级信息和考试情况，选出符合本班级的考试学生
    fpddata = fpddata[fpddata['User'].isin(df['User'])]
    df = df[df['User'].isin(fpddata['User'])]
