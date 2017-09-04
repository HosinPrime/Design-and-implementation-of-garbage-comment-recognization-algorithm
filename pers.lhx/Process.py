# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 11:23:17 2017

@author: Administrator
"""

def cmp(s,x1,y1,x2,y2):
    len1 = y1 - x1 + 1
    len2 = y2 - x2 + 1
    if len1 != len2: 
        return False
    i = x1
    j = x2
    while i <= y1:
        if s[i] != s[j]:
            return False
        i = i + 1
        j = j + 1
    return True

def add(start,end,delete):
    i = start
    while i <= end:
        delete.append(i)
        i = i+1



def compressFront(s):
    delete = []
    p1 = -1
    p2 = -1
    p3 = -1
    p4 = -1
    for i in range(len(s)):
        if p1 == -1:
          #  print("p1初始")
            p1 = i
            p2 = i
        elif s[i] != s[p1]:
            if p3 == -1:
           #     print("p3未初始1")
                p2 = i
            else:
                if(cmp(s,p1,p2,p3,p4)):
             #       print("压缩去词1")
                    add(p3,p4,delete)
                    p1 = i
                    p2 = i                     #可以可以可以可以
                    p3 = -1
                    p4 = -1
                else:
             #       print("第一种情况")
                    p4 = i
        elif s[i] == s[p1]:
                if p3 == -1:
                #    print("p3未初始2")
                    p3 = i
                    p4 = i
                else:
                    if(cmp(s,p1,p2,p3,p4)):
                 #       print("压缩去词2")
                        add(p3,p4,delete)
                        p3 = i
                        p4 = i
                    else:
                  #      print("第二种情况")
                        p3 = -1
                        p4 = -1
                        p1 = i
                        p2 = i

    if cmp(s,p1,p2,p3,p4):
        add(p3,p4,delete)
        
    tmp = ""
    for i in range(len(s)):
        if i in delete:
            continue
        else:
            tmp = tmp + s[i]
            
    return tmp

def compressBack(s):
    delete = []
    p1 = -1
    p2 = -1
    p3 = -1
    p4 = -1
    for i in range(len(s))[::-1]:
        if p1 == -1:
          #  print("p1初始")
            p1 = i
            p2 = i
        elif s[i] != s[p1]:
            if p3 == -1:
           #     print("p3未初始1")
                p2 = i
            else:
                if(cmp(s,p2,p1,p4,p3)):
             #       print("压缩去词1")
                    add(p4,p3,delete)
                    p1 = i
                    p2 = i                     #可以可以可以可以
                    p3 = -1
                    p4 = -1
                else:
             #       print("第一种情况")
                    p4 = i
        elif s[i] == s[p1]:
                if p3 == -1:
                #    print("p3未初始2")
                    p3 = i
                    p4 = i
                else:
                    if(cmp(s,p2,p1,p4,p3)):
                 #       print("压缩去词2")
                        add(p4,p3,delete)
                        p3 = i
                        p4 = i
                    else:
                  #      print("第二种情况")
                        p3 = -1
                        p4 = -1
                        p1 = i
                        p2 = i

    if cmp(s,p2,p1,p4,p3):
        add(p4,p3,delete)
        
    tmp = ""
    for i in range(len(s)):
        if i in delete:
            continue
        else:
            tmp = tmp + s[i]
            
    return tmp

def compress(s):
    tmp = compressFront(s)
    return compressBack(tmp)
