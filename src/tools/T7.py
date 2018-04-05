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

def run(codes,dh):
    # if len(dh.get_buyed()) > 0:
    #    for code in dh.get_buyed():
    #        if code in codes:
    #           codes.remove(code)
    try:
        # if len(codes) > 0: 
        #    df = ts.get_realtime_quotes(codes)
        #    dh.addData(df)
        #    res = analyze.calcMain(dh)
        #    if res != '':
        #       dh.add_buyed(res)
           print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))    
           print(codes)
    except Exception as e:
           MyLog.error('get data error %s %s' % (codes,str(e)))
    finally:               
           global timer
           timer = threading.Timer(setting.get_t1()['get_data_inter'], run, args=[codes,dh])
           timer.start()

threads = []
codes = get_today_all_codes()
length = len(codes)
begin = 0
num_threads = length // 100 + 1
for i in range(num_threads):
    end = begin + 100
    if end > length:
       end = length 
    df_codes = codes[begin:end]
    code_list = df_codes.tolist()
    for code in setting.get_ignore():
        if code in code_list:
           code_list.remove(code)  
    dh = DataHolder(code_list)
    t = threading.Thread(target=run, args=(code_list,dh))   
    t.setDaemon(True)
    t.start()
    threads.append(t)
    begin = end
    if begin >= length:
       break
    for t in threads:
        t.join()  

while True:
      time.sleep(1)
pass