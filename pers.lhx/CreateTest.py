# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:22:33 2017

@author: Administrator
"""

f1 = open('../data/train_good.txt','w')
f2 = open('../data/train_bad.txt','w')
with open('../data/data2train.txt','r',errors='ignore') as f:
    for line in f.readlines():
        sp = line.strip().split('\t',1)
        if int(sp[0]) == 0:
            f1.write(sp[0] + '\t' + sp[1] + '\n')
        else:
            f2.write(sp[0] + '\t' + sp[1] + '\n')

f1.close()
f2.close()

f1 = open('../data/test_good.txt','w')
f2 = open('../data/test_bad.txt','w')
with open('../data/data2test.txt','r',errors='ignore') as f:
    for line in f.readlines():
        sp = line.strip().split('\t',1)
        if int(sp[0]) == 0:
            f1.write(sp[0] + '\t' + sp[1] + '\n')
        else:
            f2.write(sp[0] + '\t' + sp[1] + '\n')

f1.close()
f2.close()
