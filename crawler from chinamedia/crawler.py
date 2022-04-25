#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 21:44:11 2021

@author: yangyichen
"""
#載入使用套件
#pip install tomorrow

# 爬蟲類套件
import requests
import json
from bs4 import BeautifulSoup
# 加入使用者資訊(如使用什麼瀏覽器、作業系統...等資訊)模擬真實瀏覽網頁的情況
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
from tomorrow import threads
# 資料整理類套件
import pandas as pd
import re
from datetime import datetime
# 其他
import os

#擷取一篇新聞
def GetNews_chinatimes(response):
    soup = BeautifulSoup(response.text,features="lxml")
    url = soup.find('link')['href']
    ndf = pd.DataFrame(data = [{'TITLE':soup.find('h1', attrs={'class':'article-title'}).text,
                                'TIME':datetime.strptime(soup.find('meta', attrs={'property':'article:published_time'})['content'],'%Y-%m-%dT%H:%M:%S+08:00'),
                                'CATEGORY':soup.find('meta',attrs={'property':'article:section'})['content'],
                                'DESCRIPTION':soup.find('meta',attrs={'name':'description'})['content'],
                                'CONTENT':'\n'.join(i.text for i in soup.find('div',attrs={'class':'article-body'}).find_all('p')),
                                'FROM':soup.find('meta',{'name':'publisher'})['content'],
                                'LINK':soup.find('meta', {'property':'og:url'})['content']}],
                       columns = ['TITLE', 'TIME', 'CATEGORY', 'DESCRIPTION', 'CONTENT','KEYWORDS', 'FROM', 'LINK']) 
    return ndf


#擷取特定關鍵詞新聞的連結清單
def GetLinks_chinatimes(response):
    links = []
    soup = BeautifulSoup(response.text)
    for i in soup.find_all('h3'):
        url = i.find('a')['href']
        links.append(url)
    return links

#開啟多線程功能
@threads(5)
def MultiThread_Crawl(url):
    try:
        return requests.get(url, headers=headers)
    except:
        pass

#組合應用
def CrawlNews_chinatimes(keywords, pages):
    # 截取多個分頁的新聞連結
    links = []
    for i in range(pages):
        url = 'https://www.chinatimes.com/search/{}?page={}&chdtv'.format(keywords, i+1)
        resp = requests.get(url)
        links += GetLinks_chinatimes(resp)
        links = list(set(links))  
        print('There are {} links in page {}.'.format(len(links),str(i)))

    # 多線程爬蟲
    responses = [MultiThread_Crawl(link) for link in links]

    # 整理成DataFrame
    list_of_dataframes = []
    for response in responses:
        try:
            ndf = GetNews_chinatimes(response)
            list_of_dataframes.append(ndf)
        except:
            pass
    df = pd.concat(list_of_dataframes, ignore_index=True)
    print('There are {} News in DataFrame.'.format(len(df)))
    return df

# 可以自行替換查詢的關鍵字，另外需要更多新聞的人也可以把 pages 的數值調高)
df = CrawlNews_chinatimes(keywords='台積電2330', pages=10)
#print(df)
df.to_csv("2330news.csv")