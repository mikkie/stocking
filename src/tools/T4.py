# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import math
import threading
import time
import pandas as pd
from datetime import datetime

datas = {}

def calcTime(date,timeA,timeB):
    d1 = datetime.strptime(date + ' ' + timeA, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(date + ' ' + timeB, '%Y-%m-%d %H:%M:%S')
    delta = d1 - d2
    return delta.seconds

def calculate():
    df = ts.get_realtime_quotes(['300698','000617','601375','002736','300708','603611'])
    rowList = []
    for index,row in df.iterrows():
        code = row['code']
        if code in datas:
           run = True
           if datas[code]['now'] is not None:
              lastTime = datas[code]['now'].iloc[-1].get('time') 
              if lastTime == row['time']:
                 run = False 
           if run:
              now = datas[code]['now'].append(row)
              datas[code]['previous'] = datas[code]['now']
              datas[code]['now'] = now
        else:
           datas[code] = {'previous' : None, 'now' : pd.DataFrame([row])}
        if datas[code]['previous'] is not None and len(datas[code]['previous']) >= 5:
           last = datas[code]['previous'].iloc[-5]
           last_p = (float(last['price']) - float(last['pre_close'])) / float(last['pre_close']) * 100
           now = datas[code]['now'].iloc[-1]
           now_p = (float(now['price']) - float(now['pre_close'])) / float(now['pre_close']) * 100
           deltTime = calcTime(now['date'],now['time'],last['time'])
           if deltTime == 0:
              continue 
           v_avg = (now_p - last_p) / deltTime
           s = 10 - now_p
           if s <=0:
              continue 
           t = float('Inf')
           if v_avg != 0:
              t = s / v_avg
           now['predict_time'] = t 
           if t > 0 and not math.isinf(t):
              rowList.append(now)   
    if len(rowList) > 0:
       df = pd.DataFrame(rowList)
       df = df.sort_values(by='predict_time')
       print(df)


    timer2 = threading.Timer(1, calculate)
    timer2.start()

timer2 = threading.Timer(1, calculate)
timer2.start()

while True:
      time.sleep(0.01)
pass