# -*-coding=utf-8-*-
__author__ = 'aqua'
#从tushare实时获取数据
import tushare as ts
import threading
import time
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append('..')
from config.Config import Config
from t1.datas.DataHolder import DataHolder
from t1.analyze.Analyze import Analyze

codes = ['601901','002736']
datas = {}
setting = Config()
engine = create_engine(setting.get_DBurl())
dh = DataHolder(codes,setting.get_t1()['need_save_data'],setting.get_t1()['need_recover_data'])
analyze = Analyze()

def addData(df):
    dh.addData(df)
    analyze.calcMain(dh)

def getData():
    df = ts.get_realtime_quotes(codes)
    addData(df)
    global timer
    timer = threading.Timer(setting.get_t1()['get_data_inter'], getData)
    timer.start()

timer = threading.Timer(setting.get_t1()['get_data_inter'], getData)
timer.start()

while True:
      time.sleep(1)
pass