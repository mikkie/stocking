# -*-coding=utf-8-*-
__author__ = 'aqua'

cont = ['医疗改革','医药电商']
res = []
f = open("../../data/gndata.txt",encoding="utf-8")              
contName = f.readline().strip()               
while contName:   
      line = f.readline().strip()
      if contName in cont:                   
         res.append(line)
      contName = f.readline().strip() 
f.close()
print(','.join(res))
