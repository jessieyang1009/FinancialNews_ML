#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 22:00:47 2021

@author: yangyichen
"""

import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix

path="/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/label/table_label.csv"
path2="/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/label/table.csv"
data = pd.read_csv(path,index_col="news")
table = pd.read_csv(path2,index_col="news")
#將資料切割訓練及測試
X = table
y = np.array(data["label"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state=101)


clf = tree.DecisionTreeClassifier()  #使用tree套件中的cart模組
f = clf.fit(X_train,y_train)  # fit()求得訓練集X的均值(訓練過程)

#import pydotplus
#dot_data = tree.export_graphviz(clf, out_file=None)
#graph = pydotplus.graph_from_dot_data(dot_data)
#graph.write_pdf("cart.pdf")

predictions = clf.predict(X_test)  #建立預測模組
print(confusion_matrix(y_test,predictions,labels=[1,0]))
print('--------------------------------------------')
print(classification_report(y_test,predictions,labels=[1,0]))