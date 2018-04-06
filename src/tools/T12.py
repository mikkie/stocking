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
from t1.analyze.SellAnalyze import SellAnalyze
from t1.trade.MockTrade import MockTrade
from t1.MyLog import MyLog
from utils.Utils import Utils
from sqlalchemy import create_engine
import multiprocessing as mp
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

codeList = []
setting = Config()
mockTrade = MockTrade()
engine = create_engine(setting.get_DBurl())
analyze = SellAnalyze()


def run(queue):
    MyLog.info('child process %s is running' % os.getpid())
    try:
        dh = None
        data = queue.get(True)
        while data is not None and data['df'] is not None and len(data['df']) > 0:
            df = data['df']
            s = int(round(time.time() * 1000))
            if dh is None:
               codeList = df['code'].tolist()
               dh = DataHolder(codeList) 
            dh.addData(df)
            analyze.calcMain(dh)
            MyLog.debug('process %s, calc data time = %d' % (os.getpid(),(int(round(time.time() * 1000)) - s))) 
            data = queue.get(True)   
    except Exception as e:
        MyLog.error('error %s' % str(e))

if __name__ == '__main__':
   MyLog.info('main process %s.' % os.getpid())
   mockTrade.relogin()
   pool = mp.Pool(1)
   manager = mp.Manager()
   queue = manager.Queue()
   pool.apply_async(run, (queue,))
   sched = BlockingScheduler()
   interDataHolder = {
      'currentTime' : dt.datetime.now()
   }

   @sched.scheduled_job('interval', seconds=setting.get_t1()['get_data_inter'])
   def getData():
       now = dt.datetime.now()
       if (now - interDataHolder['currentTime']).seconds > 60:
          interDataHolder['currentTime'] = now
          mockTrade.relogin()
       df = ts.get_realtime_quotes(codeList)
       queue.put({'df' : df})

   sched.start()