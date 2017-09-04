# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:41:25 2017

@author: Administrator
"""
import Process

f = open('../data/train_process2.txt')
f1 = open('../data/train_process3.txt','w')

while True:
    line = f.readline().strip()
    if line:
        sp = line.split('\t',1)
        line = sp[1]
        line = Process.compress(line)
        f1.write(sp[0] + '\t' + line + "\n")
    else:
        break
f.close()
f1.close()

f = open('../data/test_process2.txt')
f1 = open('../data/test_process3.txt','w')

while True:
    line = f.readline().strip()
    if line:
        sp = line.split('\t',1)
        line = sp[1]
        line = Process.compress(line)
        f1.write(sp[0] + '\t' + line + "\n")
    else:
        break
f.close()
f1.close()
