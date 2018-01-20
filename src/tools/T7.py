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

codes = ['601901','002736']
setting = Config()
dh = DataHolder(codes)
analyze = Analyze()

def run():
    df = ts.get_realtime_quotes(codes)
    dh.addData(df)
    analyze.calcMain(dh)
    global timer
    timer = threading.Timer(setting.get_t1()['get_data_inter'], run)
    timer.start()

timer = threading.Timer(setting.get_t1()['get_data_inter'], run)
timer.start()

while True:
      time.sleep(1)
pass