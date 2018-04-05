# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
from sqlalchemy import create_engine
import threading
import time
import sys
sys.path.append('..')
from trade.DataHolder import DataHolder
from utils.Utils import Utils
from trade.Calculate import Calculate

engine = create_engine('mysql://root:aqua@127.0.0.1/stocking?charset=utf8')
datas = {}
codeList = ['000615','300107','600159','600749','300685','300096','600729','600604','600246','002631','603177','300547','600588','300715','002155','300676','000959','601328','000686','002129','002681','002151','002161','000789','603320','300597','601313','300386','300327','300730','600760','002915','300109']
dh = DataHolder()
calc = Calculate()

def cb(**kw):
    return ts.get_tick_data(kw['kw']['code'],date='2018-01-12')

maxLength = 0

for code in codeList:
    df = Utils.queryData('tick_' + code, 'code', engine, cb, forceUpdate=False, code=code)
    net = 0
    if df is not None:
       datas[code] = df 

i = 0       

def monitoring(i):
    for code in datas:
        pos = len(datas[code]) - 1 - i
        if pos >= 0:
           dh.add_data(code,datas[code].iloc[pos]) 
    i = i + 1
        # print(dh.get_data(code))
    timer = threading.Timer(3, monitoring,[i])
    timer.start()

timer = threading.Timer(3, monitoring,[i])
timer.start()

def calculate(dh):
    calc.calc(codeList,dh)
    timer2 = threading.Timer(1, calculate,[dh])
    timer2.start()

timer2 = threading.Timer(1, calculate,[dh])
timer2.start()

while True:
      time.sleep(0.01)
pass
