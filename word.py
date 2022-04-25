#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 17:34:41 2021

@author: yangyichen
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 20:03:05 2020

@author: user05
"""
#用jieba做分詞
    
import os
import jieba
import jieba.analyse
import pandas as pd
import re
jieba.set_dictionary('/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/test/dict.txt.big') #改用繁體中文詞庫(預設是簡體)
jieba.load_userdict("/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學//test/user_defined_dictionary.txt")  #加入自定義詞庫
jieba.analyse.set_stop_words('/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/test/stopWords.txt')#去除停用字
index=[]


stopWords=[]#去除停用字(手動)
with open('/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/test/stopWords.txt', 'r', encoding='UTF-8') as file:  #'r'表示讀 開啟停用字檔
    for data in file.readlines(): #讀取所有行
        data = data.strip()  #刪除頭尾
        stopWords.append(data)        
checkNum = re.compile("[^0-9 /()◆◇「」（）。，『』【】;；、,.?？!！:：·‧......<>…~%％〈〉★→《》-]+")#移除數字用


path="/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/news"
files = os.listdir(path)  #獲取新聞目錄列表
for file in files:
    if "csv" not in file:
        continue  #跳過換下一個
    index.append(file)
    
for i in index:    
    store = pd.read_csv(path+"/"+i)
    #Headline = store["Headline"][0]
    Article_Content = store["Article_Content"][0]
    words = jieba.cut(Article_Content, cut_all=False)  #分詞
    remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', words))#過濾不符合定義詞庫的屬於剩餘字
    remainderWords = list(filter(checkNum.match, remainderWords))
    with open(i[:-4]+".txt", "w+",encoding="utf-8") as f:   #w+可讀寫  i[:-4]指讀到倒數第五位（.csv檔名不加入）
        for word in remainderWords:
            f.write(word+"\n")
    print(i[:-4]+".txt is saved")
    





    
    