# -*-coding=utf-8-*-
__author__ = 'aqua'

cont = ['互联网医疗','农机','医疗改革','智能穿戴','微信小程序','芯片概念']
res = []
f = open("../../data/gndata.txt",encoding="utf-8")              
contName = f.readline().strip()               
while contName:   
      line = f.readline().strip()
      if contName in cont:                   
         res.append(line)
      contName = f.readline().strip() 
f.close()
result = ','.join(res)
f = open("../extend/ltg.py",encoding="utf-8")
origin = f.read()
f.close()
f = open("../extend/ltgres.py", 'w')
origin = origin.replace('code_content',result)
f.write(origin)
f.close()
