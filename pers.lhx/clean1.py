# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:11:59 2017

@author: Administrator
"""
import re

f = open('../data/train.txt',errors='ignore')
f1 = open('../data/train_process1.txt','w')
while True:
    try:
        line = f.readline().strip()
    except:
        continue
    if line:
        sp = line.split("\t",1)
        line = sp[1]
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        if len(line) == 0:
            continue
        f1.write(sp[0] + '\t' + line + '\n')
    else:
        break
f.close()
f1.close()

f = open('../data/test.txt',errors='ignore')
f1 = open('../data/test_process1.txt','w')
while True:
    try:
        line = f.readline().strip()
    except:
        continue
    if line:
        sp = line.split("\t",1)
        line = sp[1]
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        if len(line) == 0:
            continue
        f1.write(sp[0] + '\t' + line + '\n')
    else:
        break
f.close()
f1.close()

