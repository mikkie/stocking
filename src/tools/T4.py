# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
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
    df = ts.get_realtime_quotes(['600025'])
    rowList = []
    for index,row in df.iterrows():
        code = row['code']
        if code in datas:
           run = True
           if datas[code]['previous'] is not None:
              lastTime = datas[code]['previous'].iloc[-1].get('time') 
              if lastTime == row['time']:
                 run = False 
           if run:
              now = datas[code]['now'].append(row)
              datas[code]['previous'] = datas[code]['now']
              datas[code]['now'] = now
        else:
           datas[code] = {'previous' : None, 'now' : pd.DataFrame([row])}
        if datas[code]['previous'] is not None and len(datas[code]['previous']) >= 6:
           last = datas[code]['previous'].iloc[-4]
           last1 = datas[code]['previous'].iloc[-5]
           last_p = (last['close'] - last['pre_close'] / last['pre_close'])
           last1_p = (last1['close'] - last1['pre_close'] / last1['pre_close'])
           v0 = (last_p - last1_p) / calcTime(last['date'],last['time'],last1['time'])
           now = datas[code]['now'].iloc[-1]
           before = datas[code]['now'].iloc[-2]   
           now_p = (now['close'] - now['pre_close'] / now['pre_close'])
           before_p = (before['close'] - before['pre_close'] / before['pre_close'])
           v1 = (now_p - before_p) / calcTime(now['date'],now['time'],before['time'])
           s = 10 - (now['close'] - now['pre_close'] / now['pre_close'])
           v_avg = (v0 + v1) / 2
           t = float('Inf')
           if v_avg != 0:
              t = s / v_avg
           now['predict_time'] = t 
        rowList.append(now)   
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