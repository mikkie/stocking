# -*-coding=utf-8-*-
__author__ = 'aqua'
#Mock数据
import tushare as ts
import threading
import time
import datetime as dt
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append('..')
from config.Config import Config 
from t1.MyLog import MyLog
from t1.datas.NewDataHolder2 import NewDataHolder2
from t1.analyze.NewAnalyze2 import NewAnalyze2
# from t1.analyze.Concept import Concept
# from t1.analyze.NetMoney import NetMoney

codes = ['000019']
src_datas = {}
datas = {}
setting = Config()
engine = create_engine(setting.get_DBurl())
dh = NewDataHolder2()
analyze = NewAnalyze2()

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
    if len(df) > 0:
       dh.addData(df)
       codes = analyze.calcMain(None,dh,dt.datetime.now(),None,None)

for i in range(5200):
    run(i)

input('please enter to exit')    
