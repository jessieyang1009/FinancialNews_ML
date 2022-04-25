#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 22:46:17 2021

@author: yangyichen
"""

#標出label的值
import os
import pandas as pd #Data Analysis Library像個excel

path_n = "/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/news" 
index_n = []
files_n = os.listdir(path_n) #獲取新聞目錄列表
for file in files_n:   #不是csv檔
    if "csv" not in file:
        continue   #跳過不處理
    else:
        index_n.append(file)   #加入到序列當中
        
path_s = "/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/stock" #股票路徑    
index_s = []
files_s = os.listdir(path_s)  #獲取股票目錄列表     
for file in files_s:
    if "csv" not in file:   #不是csv檔
        continue
    else:
        index_s.append(file)   #加入到序列當中
                
yesterday_close = 0
result = 0
label_flag = 0
l=len(index_n)
label=[]
for stock in index_s:#開啟每個股票檔案
    data_s = pd.read_csv(path_s+"/"+stock, index_col="Date")#讀取日期
    
    for d in data_s.index:#迴圈:每個股票日期
        date_temp=d
        YMD_s_v = int(str(int(date_temp[0:3])+1911)+date_temp[4:6]+date_temp[7:9]) 
			#股價時間（民國年轉西元年＋月份＋日期）
        YMD_s = str(int(date_temp[0:3])+1911)+"-"+date_temp[4:6]+"-"+date_temp[7:9] 
			#以字串格式儲存西元年-月份-日期
        today_open = data_s.at[d,"Opening price"]  #開盤價 dataframe獲取指定位置用at
        today_close = data_s.at[d,"Closing price"] #關盤價
        moring_result = today_close - today_open
        other_result = today_close - yesterday_close
        while len(index_n)>0:  #新聞列表
            top_news=index_n[0]
            #print(top_news)
            YMD_n_v = int(top_news[0:4]+top_news[5:7]+top_news[8:10]) #新聞時間
            if YMD_s_v < YMD_n_v:
                break
            elif YMD_s_v ==  YMD_n_v:
                data_n = pd.read_csv(path_n+"/"+top_news) #讀取新聞資料
                date_temp = data_n.at[0,"Post_Date_Time"] #新聞發布的日期
                hour = date_temp[11:13] #新聞發布的時間
                mins = date_temp[14:16]
                if int(hour) >= 9 and int(hour) <=13: #介於股市開盤時間
                    result = moring_result
                elif int(hour) == 13 and int(mins) <=30:  #介於股市開盤時間
                    result = moring_result
                else:
                    result = other_result
                
                if result > 0:
                    label_flag = 1  #若有結果就標記1
                else:
                    label_flag = 0
                label.append(label_flag)
                index_n.remove(top_news) #移除第一個往下繼續搜尋
                
            elif YMD_s_v > YMD_n_v:
                result = other_result
                if result > 0:
                    label_flag = 1
                else:
                    label_flag = 0
                label.append(label_flag)
                index_n.remove(top_news)
                
        yesterday_close = today_close

        
table = pd.read_csv("/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/label/table.csv",index_col="news")
table["label"]=label
table.to_csv("table_label.csv") #將資料保存在table_label.csv中
os.getcwd()  #獲取路徑