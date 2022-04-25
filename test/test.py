# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:54:44 2020

@author: Holic
"""

import jieba
import jieba.analyse
import re
jieba.set_dictionary('dict.txt.big') #改用繁體中文詞庫(預設是簡體)
jieba.load_userdict("user_defined_dictionary.txt")
jieba.analyse.set_stop_words('stop_Words.txt')
Article_Content="【鉅亨網新聞中心】第二條　第12款符合條款第二條第XX款：12事實發生日：103/05/121.召開法人說明會之日期：103/05/122.召開法人說明會之時間：16 時 00 分 3.召開法人說明會之地點：麥格里證券4.法人說明會擇要訊息：本公司將於103/5/12受邀請參加麥格里證券舉辦之投資人電話會議，會中就本公司已公開發佈之財務數字、經營績效等相關資訊做說明，詳請參閱公開資訊觀測站。5.其他應敘明事項：無完整財務業務資訊請至公開資訊觀測站之法人說明會一覽表或法說會項目下查閱。"

stopWords=[]
segments=[]
remainderWords=[]
with open('stopWords.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)
checkNum = re.compile("[^0-9 /()◆◇「」（）。，『』【】;；、,.?？!！:：·‧......<>…~%％〈〉★→《》-]+")
segments = jieba.cut(Article_Content, cut_all=False)
remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', segments))
remainderWords = list(filter(checkNum.match, remainderWords))
for word in remainderWords:
    print(word)