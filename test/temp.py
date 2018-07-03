# -*-coding=utf-8-*-
__author__ = 'aqua'

l = [1,2,3,4,5]
for i in range(20):
    if len(l) > 10:
       l.pop(0)
    l.append(i)

print(sum(l))   




