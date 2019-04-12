# -*- coding: utf-8 -*-
"""

@Author: lushaoxiao
@Date: 2019/4/8
@IDE: PyCharm
"""
from mysql import connector
import matplotlib.pyplot as plt
import numpy as np

dbuser = "root"
dbname = "orcid"
dbpassword = ""
sql = "SELECT COUNT(country),country FROM info GROUP BY country ORDER BY COUNT(country) DESC LIMIT 8"

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

if __name__ == '__main__':
    cnx = connector.connect(user=dbuser, database=dbname, password=dbpassword)
    cursor = cnx.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    cname = []
    cdata = []
    for item in data:
        cdata.append(item[0])
        cname.append(item[1])
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(cdata, autopct=lambda pct: func(pct, cdata),
                                      textprops=dict(color="w"))
    ax.legend(wedges, cname,
              title="Country",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("Country statistic")
    plt.show()

    histlabel = []
    for item in cname:
        l = ""
        for i in range(len(item)):
            if str.isupper(item[i]):
                l += item[i]
        histlabel.append(l)
    print(histlabel)
    N = 8
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(histlabel)))
    p1 = plt.bar(ind, cdata, width,color=colors)
    plt.ylabel('Numbers')
    plt.xlabel('Country')
    plt.xticks(ind,histlabel)
    plt.legend(p1,cname)
    plt.show()
