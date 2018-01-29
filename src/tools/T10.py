# -*-coding=utf-8-*-
__author__ = 'aqua'
#从tushare实时获取数据
import tushare as ts
import threading
import time
import pandas as pd
import sys
sys.path.append('..')
from config.Config import Config
from t1.datas.DataHolder import DataHolder
from t1.analyze.Analyze import Analyze
from t1.MyLog import MyLog
from utils.Utils import Utils
from sqlalchemy import create_engine

setting = Config()
engine = create_engine(setting.get_DBurl())
analyze = Analyze()

def get_today_all_codes():
    def cb(**kw):
        return ts.get_today_all()
    df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=False)
    return df_todayAll['code']

def run(codeSplits,dh):
    try:
        df_total = pd.DataFrame()
        if len(dh.get_buyed()) > 0:
           for codeList in codeSplits: 
               for code in dh.get_buyed():
                   if code in codeList:
                      codeList.remove(code)
        for codeList in codeSplits:
            if len(codeList) > 0: 
               df = ts.get_realtime_quotes(codeList)
               df_total= df_total.append(df)
        dh.addData(df_total)
        res = analyze.calcMain(dh)
        if res != '':
           dh.add_buyed(res)
    except Exception as e:
           MyLog.error('get data error %s %s' % (codes,str(e)))
    finally:               
           global timer
           timer = threading.Timer(setting.get_t1()['get_data_inter'], run, args=[codeSplits,dh])
           timer.start()

codeSplits = []
codes = get_today_all_codes()
codeLists = codes.tolist()
for code in setting.get_ignore():
    if code in codeLists:
       codeLists.remove(code)  
dh = DataHolder(codeLists)
length = len(codeLists)
begin = 0
num_splits = length // setting.get_t1()['split_size'] + 1
for i in range(num_splits):
    end = begin + setting.get_t1()['split_size']
    if end > length:
       end = length 
    code_split = codeLists[begin:end]
    codeSplits.append(code_split) 
    begin = end
    if begin >= length:
       break

run(codeSplits,dh)

