# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:29:19 2017

@author: Administrator
"""

from numpy import *
import jieba
import Process
import datetime




def createVocabList(dataSet):
    vocabSet = set([])  #创建一个空的set
    i = 1
    for document in dataSet:
        vocabSet = vocabSet | set(document) #两个set并，可以去重
        print("处理完第",i,"个set")
        i += 1
    return list(vocabSet)


    

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def loadStopWords():
    f = open('../data/StopWords.txt','r')
    words = []
    while True:
        line = f.readline().strip()
        if line:
            words.append(line)
        else:
            break
    return words

def textParse(bigString,stopWords):#
    '''
    文本切分
    输入文本字符串，输出词表
    '''
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok for tok in listOfTokens if len(tok) > 0 and tok not in stopWords]

def trainNB(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)   #垃圾的总量除以总的数据数量得到垃圾占总的比例
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones() 
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]                #该垃圾又出现了一次
            p1Denom += sum(trainMatrix[i])         #是垃圾的情况总共出现的次数
        else:
            p0Num += trainMatrix[i]                #该文本在不是垃圾的分类
            p0Denom += sum(trainMatrix[i])         #不是垃圾的文本的总的出现次数
    p1Vect = log(p1Num/p1Denom)          #change to log()  求出p(w|c1);
    p0Vect = log(p0Num/p0Denom)          #change to log()   求出p(w|c0);
    return p0Vect,p1Vect,pAbusive




def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1,threshold = 3.0):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    p0 = p0 + log(threshold)
    if p1 >  p0:
        return 1
    else: 
        return 0


def train():
    '''
    训练 函数
    '''
    now = datetime.datetime.now()
    docList=[]; classList = []; 
    stopWords = loadStopWords()
    count1 = 1
    with open('../data/train_process4.txt') as f:
        for line in f.readlines():
            sp = line.split('\t',1)
            wordList = textParse(sp[1],stopWords)
            docList.append(wordList)
            classList.append(int(sp[0]))
            print("处理完第",count1,"条数据")
            count1 += 1
    vocabList = createVocabList(docList)#生成次表库
    trainMat=[]; trainClasses = []
    count2 = 1
    for docIndex in range(len(docList)):#生成训练矩阵及标签
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
        print("训练矩阵第",count2,"行完成")
        count2 += 1
    p0V,p1V,pSpam = trainNB(array(trainMat),array(trainClasses)) 
    print("训练耗时",datetime.datetime.now() - now)
    storeTree(p0V,p1V,pSpam,vocabList,'../db/store1.txt','../db/store2.txt','../db/store3.txt','../db/store4.txt')
    print(len(vocabList))
    
def storeTree(p0V,p1V,pSpam,vocabList,file1,file2,file3,file4):
    import pickle
    fw = open(file1,'wb')
    pickle.dump(p0V,fw)
    fw.close()
    fw = open(file2,'wb')
    pickle.dump(p1V,fw)
    fw.close()
    fw = open(file3,'wb')
    pickle.dump(pSpam,fw)
    fw.close()
    fw = open(file4,'wb')
    pickle.dump(vocabList,fw)
    fw.close()

def grabTree(file1,file2,file3,file4):
    import pickle
    fr = open(file1,'rb')
    p0V = pickle.load(fr)
    fr.close()
    fr = open(file2,'rb')
    p1V = pickle.load(fr)
    fr.close()
    fr = open(file3,'rb')
    pSpam = pickle.load(fr)
    fr.close()
    fr = open(file4,'rb')
    vocabList = pickle.load(fr)
    fr.close()
    return p0V,p1V,pSpam,vocabList

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
    
def classify(s,threshold = 3.0):             
    content = classifyFirst(s)
    if len(content) == 0: return 1
    content = Process.compress(content)
    stopWords = loadStopWords()
    if len(content) < 4:
        return 1
    if  classifySecond(content):
        return 1
    p0V,p1V,pSpam,vocabList = grabTree('../db/store1.txt','../db/store2.txt','../db/store3.txt','../db/store4.txt')
    s = jieba.cut(content)
    s ="  ".join(s)   
    testEntry = textParse(s,stopWords)
    thisDoc = array(bagOfWords2VecMN(vocabList, testEntry))
    cat = classifyNB(thisDoc,p0V,p1V,pSpam,threshold)
    return cat

def test():
    now = datetime.datetime.now()
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    count = 1
    classList = []
    f = open('../data/test.txt')
    while True:
        line = f.readline().strip()
        if line:
            print("预测第",count,"条句子")
            count += 1
            sp = line.split('\t',1)
            s = sp[1]
            cat = classify(s)
            classList.append(cat)
            cl = int(sp[0])
            if cl == 0 and cat == 0:
                TP += 1
            elif cl ==0 and cat == 1:
                TN +=1
            elif cl == 1 and cat == 0:
                FP += 1
            else:
                FN += 1          
        else:
            break
    f.close()
    print("测试花费时间为：",datetime.datetime.now() - now )
    print("TP=",TP,"TN=",TN,"FN=",FN,"FP=",FP)
    accuracy =  (float(TP) + FN) / (TP + TN + FP + FN) 
    precision1 = float(TP) / (TP + FP)
    recall1 = float(TP) / (TP + TN)
    precision2 = float(FN) / (FN + TN)
    recall2 = float(FN) / (FP + FN)
    f1 = 2 * float(precision1) * recall1 / (precision1 + recall1)
    f2 = 2 * float(precision2) * recall2 / (precision2 + recall2)
    print('准确率是 %.3f' % accuracy)
    print('分类为正常评论精确率是 %.3f' % precision1)
    print('分类为正常评论召回率是 %.3f' % recall1)
    print('分类为垃圾评论精确率是 %.3f' % precision2)
    print('分类为垃圾评论召回率是 %.3f' % recall2 )
    print('分类为正常评论F1值是 %.3f' % f1)
    print('分类为垃圾评论F1值是 %.3f' % f2)
    
     
