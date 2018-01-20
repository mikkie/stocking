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
from t1.datas.DataHolder import DataHolder

datas = {}
setting = Config()
engine = create_engine(setting.get_DBurl())
dh = DataHolder(True)

def addData(df):
    dh.addData(df)

def getData():
    df = ts.get_realtime_quotes(['601901'])
    addData(df)
    global timer
    timer = threading.Timer(2, getData)
    timer.start()

timer = threading.Timer(2, getData)
timer.start()

while True:
      time.sleep(0.01)
pass