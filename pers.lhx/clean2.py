# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:58:07 2017

@author: Administrator
"""

f = open('../data/train_process1.txt')
f1 = open('../data/train_process2.txt','w')

s = set([])
count = 0
while True:
    line = f.readline()
    if line:
        count = count +1
        s.add(line)
    else:
        break
f.close()
    
for i in s:
    f1.write(i)
    


f1.close()

print("删除了%d条评论" % (count - len(s) ) ) 

f = open('../data/test_process1.txt')
f1 = open('../data/test_process2.txt','w')

s = set([])
count = 0
while True:
    line = f.readline()
    if line:
        count = count +1
        s.add(line)
    else:
        break
f.close()
    
for i in s:
    f1.write(i)
    


f1.close()

print("删除了%d条评论" % (count - len(s) ) ) 

