# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 01:24:04 2019

@author: user05
"""

import requests
from  io import StringIO
import os
import pandas as pd
import time

def crawl(date):
    r = requests.post('https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date='+str(date)+'&stockNo=2474')
    stock_data = pd.read_csv(StringIO(r.text.replace("=", "")), header=["日期" in l for l in r.text.split("\n")].index(True))
    
    stock_data.columns=['Date',
                        'Number of stocks traded','turnover','Opening price','Highest price',
                        'Lowest price','Closing price','Price difference',
                        'Number of transactions','']
    indexCol=stock_data.columns
    indexRow=stock_data.index
    stock_data.drop(indexCol[-1],axis=1,inplace=True)#移除未定義的欄位
    stock_data.drop(indexRow[-4:],inplace=True)      #移除"說明"以下的文字
    return stock_data


#year=2019
#month=12
#d=crawl(str(year)+str(month)+"01")
for i in range(2019,2013,-1):
    for j in range(12,0,-1):
        if j>9:
            d=crawl(str(i)+str(j)+"01")
            #d=pd.concat([d,tmp],axis=0)
            d.to_csv(str(i)+str(j)+".csv")
            os.getcwd()
            print(str(i)+str(j)+"get")
        else:
            d=crawl(str(i)+"0"+str(j)+"01")
            #d=pd.concat([d,tmp],axis=0)
            d.to_csv(str(i)+"0"+str(j)+".csv")
            os.getcwd()
            print(str(i)+"0"+str(j)+"get")
        time.sleep(5)                             #每5抓一次 抓太快會被鎖IP

#for i in range(3):
#    d=crawl("20200"+str(i)+"01")
#    d.to_csv("202000"+str(i)+".csv")
#    os.getcwd()
#    print("20200"+str(i)+"get")
#    time.sleep(5)


#d.to_csv("2474.csv")
#os.getcwd()

