# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import math
import threading
import time
import pandas as pd
from datetime import datetime

datas = {}

def addData(df):
    for index,row in df.iterrows():
        code = row['code']
        if code in datas:
           run = True
           if datas[code] is not None:
              lastTime = datas[code].iloc[-1].get('time') 
              if lastTime == row['time']:
                 run = False 
           if run:
              now = datas[code].append(row)
        else:
           datas[code] = pd.DataFrame([row])
        print(open_type(datas[code]))

def open_type(df):
    row = df.iloc[0]
    open_p = (float(row['price']) - float(row['pre_close'])) / float(row['pre_close']) * 100
    #高开
    if open_p > 4.0:
       return 'H_open'
    #平开
    elif open_p > -1.0 and open_p < 1.0:
         return 'F_open'
        
           

def calculate():
    df = ts.get_realtime_quotes(['300698','000617','601375','002736','300708','603611'])
    addData(df)
    timer = threading.Timer(2, calculate)
    timer.start()

timer = threading.Timer(2, calculate)
timer.start()

while True:
      time.sleep(0.01)
pass