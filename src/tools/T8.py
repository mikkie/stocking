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

codes = ['002736','600506','300698','300487','603098','300018']
src_datas = {}
datas = {}
setting = Config()
engine = create_engine(setting.get_DBurl())

for code in codes:
    src_datas[code] = pd.read_sql_table('live_' + code, con=engine)

def addData(df):
    for index,row in df.iterrows():
        code = row['code']
        if code in datas:
           lastTime = datas[code].iloc[-1].get('time') 
           if lastTime != row['time']:
              datas[code] = datas[code].append(row)
        else:
           datas[code] = pd.DataFrame([row])

def saveData():
    for code in datas:
        datas[code].to_sql('live_' + code,con=engine,if_exists='replace')
        print(datas[code])
    timer1 = threading.Timer(180, saveData)
    timer1.start()
        


def getData(i):
    df = pd.DataFrame()
    for code in src_datas:
        df.append(src_datas[code].lioc[i])
    i = i + 1    
    addData(df)
    timer = threading.Timer(2, getData,[i])
    timer.start()

timer = threading.Timer(2, getData,[0])
timer.start()

timer1 = threading.Timer(180, saveData)
timer1.start()

while True:
      time.sleep(0.01)
pass