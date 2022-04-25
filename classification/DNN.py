#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 11:13:17 2021

@author: yangyichen
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import matplotlib.pyplot as plt

path="/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/label/table_label.csv"
path2="/Users/yangyichen/Desktop/研究所/財金新聞資料分析教學/label/table.csv"
data = pd.read_csv(path,index_col="news")
table = pd.read_csv(path2,index_col="news")

#將資料切割訓練及測試
X = table
y = np.array(data["label"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state=101)


from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

#print(len(y_train))

# 在 Keras 裡面我們可以很簡單的使用 Sequential 的方法建建立一個 Model
model = Sequential()
# 加入 hidden layer-1 of 125 neurons 並指定 input_dim 為 20
model.add(Dense(125, input_dim=20))
# 使用 'relu' 當作 activation function
model.add(Activation('relu'))
# 加入 hidden layer-2 of 256 neurons
model.add(Dense(256))
model.add(Activation('relu'))
# 加入 hidden layer-3 of 256 neurons
model.add(Dense(256))
model.add(Activation('relu'))
# 加入 hidden layer-4 of 125 neurons
model.add(Dense(125))
model.add(Activation('relu'))
# 加入一個dense layer
model.add(Dense(units=1))
# 使用 'sigmoid' 當作 activation function
model.add(Activation('sigmoid'))

# 定義訓練方式  
model.compile(loss='binary_crossentropy', 
              optimizer='adam', 
              metrics=['acc',f1_m,precision_m, recall_m])

model.summary()

# 開始訓練  
train_history = model.fit(x=X_train,  
                          y=y_train, validation_split=0.1,  
                          epochs=200, batch_size=32, verbose=1)

#print(train_history.history.keys())

# summarize history for accuracy
plt.plot(train_history.history['acc'])
plt.plot(train_history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss 
plt.plot(train_history.history['loss']) 
plt.plot(train_history.history['val_loss']) 
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left') 
plt.show()
# summarize history for others
plt.plot(train_history.history['f1_m']) 
plt.plot(train_history.history['precision_m']) 
plt.plot(train_history.history['recall_m']) 
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['f1', 'precision','recall'], loc='upper left') 
plt.show()

predictions = model.predict(X_test)  #建立預測模組
print(confusion_matrix(y_test,predictions.astype(int),labels=[1,0]))
print('--------------------------------------------')
print(classification_report(y_test,predictions.astype(int),labels=[1,0]))