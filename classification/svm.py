#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 17:41:14 2021

@author: yangyichen
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report,confusion_matrix


#/Users/yangyichen/Downloads/2474/label/table_label.csv
path="/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/label/table_label.csv"
path2="/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/label/table.csv"
data = pd.read_csv(path,index_col="news")
table = pd.read_csv(path2,index_col="news")
#將資料切割訓練及測試
X = table
y = np.array(data["label"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state=101)


model = SVC()
#使用Support Vector Classifier來建立模型
model.fit(X_train,y_train) #.fit()訓練過遲

predictions = model.predict(X_test) #模型預測
#載入classification_report & confusion_matrix來評估模型好壞
print(confusion_matrix(y_test,predictions,labels=[1,0]))
print('--------------------------------------------')
print(classification_report(y_test,predictions,labels=[1,0]))

