# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:53:27 2017

@author: Administrator
"""

import time
import numpy as np


from sklearn.feature_extraction.text import  CountVectorizer

from sklearn.naive_bayes import MultinomialNB  
from sklearn.svm import LinearSVC


import pickle

def loadStopWords():
    words = []
    with open('../data/StopWords.txt','r') as f:
        for line in f.readlines():
            words.append(line.strip())
    return words


def loadTrainData():
    docList=[]; classList = [];
    with open('../data/train_process4.txt') as f:
        for line in f.readlines():
            sp = line.strip().split('\t',1)
            classList.append(int(sp[0]))
            docList.append(sp[1])
    return classList,docList

def loadTestData():
    docList = [];classList = [];
    with open('../data/test_process4.txt') as f:
        for line in f.readlines():
            sp = line.strip().split('\t',1)
            classList.append(int(sp[0]))
            docList.append(sp[1])
    return classList,docList

def getVocabulary(trainData):
    stopWords = loadStopWords()
    vectorizer = CountVectorizer(stop_words = stopWords)
    vectorizer.fit_transform(trainData)
    return vectorizer

def svm(trainData,trainLabel):
    t0 = time.time()
    stopWords = loadStopWords()
    vectorizer = CountVectorizer(stop_words = stopWords)
    fea_train = vectorizer.fit_transform(trainData)  
#    print ('Size of fea_train:' + repr(fea_train.shape)) 
    clf = LinearSVC( C= 0.8)
    clf.fit(fea_train,np.array(trainLabel))
    t1 = time.time()
    print("SVM训练用时",t1 - t0)    
    return clf
    
def nb(trainData,trainLabel):
    t0 = time.time()
    stopWords = loadStopWords()
    vectorizer = CountVectorizer(stop_words = stopWords)
    fea_train = vectorizer.fit_transform(trainData)   
 #   print ('Size of fea_train:' + repr(fea_train.shape)) 
    clf = MultinomialNB(alpha = 0.01)   
    clf.fit(fea_train,np.array(trainLabel))
    t1 = time.time()
    print("nb训练用时",t1 - t0)
    return clf

    
def train(trainData,trainLabel):
    vectorizer = getVocabulary(trainData)
    clf1 = svm(trainData,trainLabel)
    clf2 = nb(trainData,trainLabel)
    with open('../db/dic.txt','wb') as f:
        pickle.dump(vectorizer,f)
    with open('../db/svm.txt','wb') as f:
        pickle.dump(clf1,f)
    with open('../db/nb.txt','wb') as f:
        pickle.dump(clf2,f)
 
def loadClassify():
    with open('../db/dic.txt','rb') as f:
        vectorizer = pickle.load(f)
    with open('../db/svm.txt','rb') as f:
        clf1 = pickle.load(f)
    with open('../db/nb.txt','rb') as f:
        clf2 = pickle.load(f)
    return vectorizer,clf1,clf2
    

def classify(pred1,pred2):
    pred = pred1 + pred2
    for i in range(len(pred)):
        if pred[i] >= 2:
            pred[i] = 1
        else:
            pred[i] = 0
    return pred
 
def test(testData,testLabel):
    vectorizer,clf1,clf2 = loadClassify()
    fea_test = vectorizer.transform(testData)
    pred1 = clf1.predict(fea_test)
    pred2 = clf2.predict(fea_test)
    pred = classify(pred1,pred2)
    totalScore(pred1,testLabel)
    totalScore(pred2,testLabel)
    totalScore(pred,testLabel)
    
def change(s):
    news = ''    
    for i in range(len(s)):
        if s[i]>= u"\u4e00" and s[i]<= u"\u9fa6":
            news += s[i]
        else:          
            continue
    return news

def classifyFirst(s):
    news = change(s)
    return news

def classifySecond(speak):
    dirty = ['fuck','狗日的','犊子','麻批','仙人板板','R你妈','操你','草你','我日你妈','意淫']
    di = set([])
    f = open('../db/keywords (2).txt')
    while True:
        line = f.readline()
        if line:
            line = line.strip()
            if(len(line) > 1):
                di.add(line)
        else:
            break
    f.close
    dirty.extend(di)
    count = 1
    s = 0
    for i in dirty:
        if i in speak:
            s += len(i)
            count += 1
    average = s / float(count)
    length = len(speak)
    p = average / float(length)    
    if p  > 0.1:
        return 1
    else:
        return 0


def classifySentence(s,choice): #选择 1 代表SVM，2代表nb ,3代表混合
    import jieba
    import Process
    s = classifyFirst(s)
    if len(s) == 0: return 1
    s = Process.compress(s)
    if len(s) < 4:
        return 1
    if  classifySecond(s):
        return 1
    testData = []
    vectorizer,clf1,clf2 = loadClassify()
    s = " ".join(jieba.cut(s))
    print(s)
    testData.append(s)
    fea_test = vectorizer.transform(testData)
    pred1 = clf1.predict(fea_test)
    pred2 = clf2.predict(fea_test)
    pred =  classify(pred1,pred2)
    print(pred1)
    print(pred2)
    print(pred)
    if choice == 1:
        return pred1[0]
    elif choice == 2:
        return pred2[0]
    else:
        return pred[0]
    
def lhx(s,choice = 3):
    if choice not in [1,2,3]:
        print("请选择一个分类器，1-SVM,2-NB,3-MIX")
        return 
    a = classifySentence(s,choice)
    if a == 1:
        print("是垃圾评论")
    else:
        print("非垃圾评论")



def totalScore(pred,y_test):
    TP = 1
    TN = 1
    FP = 1
    FN = 1
    for i in range(len(pred)):
        if y_test[i] == 0:
            if pred[i] == 0:
                TP += 1
            elif pred[i] == 1:
               TN += 1
        elif y_test[i] == 1:
            if pred[i] == 0:
                FP += 1
            elif pred[i] == 1:
                FN +=1

    
    accuracy = 1.0 * (TP + FN) / (TP + TN + FN + FP)
    rb_precision = 1.0*FN/(TN+FN)
    rb_recall = 1.0*FN/(FN+FP)
    nor_precision = 1.0*TP/(TP+FP)
    nor_recall = 1.0*TP/(TP+TN)
    
    F1 = 2.0 * nor_precision * nor_recall / (nor_precision + nor_recall)
    F2 = 2.0 * rb_precision * rb_recall / (rb_precision + rb_recall)
    print("TP=",TP,"TN=",TN,"FN=",FN,"FP=",FP)
    print('准确率是 %.3f' % accuracy)
    print('分类为正常评论精确率是 %.3f' % nor_precision)
    print('分类为正常评论召回率是 %.3f' % nor_recall)
    print('分类为垃圾评论精确率是 %.3f' % rb_precision)
    print('分类为垃圾评论召回率是 %.3f' % rb_recall )
    print('分类为正常评论F1值是 %.3f' % F1)
    print('分类为垃圾评论F1值是 %.3f' % F2)

    











    