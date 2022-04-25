#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 20:24:07 2021

@author: yangyichen
"""

#製作關鍵字表格
import os
import pandas as pd

path_w = "/Users/yangyichen/Desktop/研究所/新聞分析教學/word"

index_w = []

files_w = os.listdir(path_w) #獲取字詞列表

for file in files_w:
    if "txt" not in file:
        continue
    elif "o" in file:
        continue
    elif "b" in file:
        continue
    else:
        index_w.append(file)


        
col = ["news","漲","佳","好","穩","正","惠","效益","升","樂觀","增","跌","壓力","弱","不足","逆","降","挫","衝擊","悲","減"]
table = pd.DataFrame(columns=col) #以col創建dataframe

for item in range (len(index_w)):    
    temp_list = ["name",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    news_name = index_w[item]
    temp_list[0]=news_name   #設定第0格為名稱
    file_path=path_w+"/"+index_w[item]
    f = open(file_path, encoding="utf-8") #讀取資料路徑
    for line in f.readlines():
        for i in range(1,21):  #在1～20欄中
            if col[i] in line:  
                temp_list[i]=1   #標記為1
    insert_row = pd.DataFrame([temp_list],columns=col)  #插入行
    table=table.append(insert_row)
table.set_index("news",inplace=True)  #set_index方法，可以設置單索引和複合索引
#table.sort_values(by=['news'],ascending=True)
table.sort_values(["news"], ascending=True)
table.to_csv("2474table.csv")
os.getcwd()
     
        