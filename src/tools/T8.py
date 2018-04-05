# -*-coding=utf-8-*-
__author__ = 'aqua'
#Mock数据
import tushare as ts
import threading
import time
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append('..')
from config.Config import Config 
from trade.Analyze import Analyze
from t1.MyLog import MyLog

codes = ['300487']
src_datas = {}
datas = {}
setting = Config()
analyze = Analyze()
engine = create_engine(setting.get_DBurl())
from t1.datas.DataHolder import DataHolder
from t1.analyze.Analyze import Analyze

dh = DataHolder(codes)
analyze = Analyze()

for code in codes:
    try:
       src_datas[code] = pd.read_sql_table('live_' + code, con=engine)
    except Exception as e:
           MyLog.error('read mock data error \n')
           MyLog.error(str(e) +  '\n')   

def run(i):
    df = pd.DataFrame()
    for code in src_datas:
        if i < len(src_datas[code]):
           df = df.append(src_datas[code].iloc[i])
    dh.addData(df)
    analyze.calcMain(dh)
    i = i + 1    
    global timer 
    timer = threading.Timer(setting.get_t1()['get_data_inter'], run,[i])
    timer.start()

timer = threading.Timer(setting.get_t1()['get_data_inter'], run,[0])
timer.start()

while True:
      time.sleep(1)
pass