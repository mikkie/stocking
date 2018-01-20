# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import threading
import time
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append('..')
from config.Config import Config 
from trade.Analyze import Analyze

codes = ['002736','600506','300698','300487','603098','300018']
src_datas = {}
datas = {}
setting = Config()
analyze = Analyze()
engine = create_engine(setting.get_DBurl())

for code in codes:
    src_datas[code] = pd.read_sql_table('live_' + code, con=engine)

def addData(df):
    for index,row in df.iterrows():
        code = row['code']
        if code in datas:
           lastTime = datas[code]['data'].iloc[-1].get('time') 
           if lastTime != row['time']:
              datas[code]['data'] = datas[code]['data'].append(row)
        else:
           datas[code] = {}
           datas[code]['data'] = pd.DataFrame([row])
           print('')

def analyzeData():
    analyze.calc(datas)
    timer1 = threading.Timer(1, analyzeData)
    timer1.start()
        


def getData(i):
    df = pd.DataFrame()
    for code in src_datas:
        if i < len(src_datas[code]):
           df = df.append(src_datas[code].iloc[i])
    i = i + 1    
    addData(df)
    timer = threading.Timer(0.1, getData,[i])
    timer.start()

timer = threading.Timer(0.1, getData,[0])
timer.start()

timer1 = threading.Timer(1, analyzeData)
timer1.start()

while True:
      time.sleep(1)
pass