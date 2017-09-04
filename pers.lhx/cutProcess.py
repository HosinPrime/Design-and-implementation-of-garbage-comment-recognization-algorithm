# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:07:02 2017

@author: Administrator
"""
import jieba

f = open('../data/train_process3.txt')
f1 = open('../data/train_process4.txt','w')

while True:
    line = f.readline().strip()
    if line:
        sp = line.split('\t',1)
        line = sp[1]
        line = " ".join(jieba.cut(line))
        f1.write(sp[0] + '\t' + line + '\n')
        
    else:
        break
f.close()
f1.close()

f = open('../data/test_process3.txt')
f1 = open('../data/test_process4.txt','w')

while True:
    line = f.readline().strip()
    if line:
        sp = line.split('\t',1)
        line = sp[1]
        line = " ".join(jieba.cut(line))
        f1.write(sp[0] + '\t' + line + '\n')
        
    else:
        break
f.close()
f1.close()


