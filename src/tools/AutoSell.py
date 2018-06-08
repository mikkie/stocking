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

codeList = ['002208','601619','300549','002909','000532']
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
            zs = data['zs']
            s = int(round(time.time() * 1000))
            if dh is None:
               codeList = df['code'].tolist()
               dh = DataHolder(codeList) 
            dh.addSellData(df)
            analyze.calcMain(zs,dh)
            MyLog.debug('process %s, calc data time = %d' % (os.getpid(),(int(round(time.time() * 1000)) - s))) 
            data = queue.get(True)   
    except Exception as e:
        MyLog.error('error %s' % str(e))

if __name__ == '__main__':
   MyLog.info('main process %s.' % os.getpid())
   strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
   while strTime < '09:30:01':
         time.sleep(0.1)
         strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
   if setting.get_t1()['trade']['enableMock']:      
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
       if setting.get_t1()['trade']['enableMock']:
          now = dt.datetime.now()
          if (now - interDataHolder['currentTime']).seconds > 60:
             interDataHolder['currentTime'] = now
             mockTrade.relogin()
       df = ts.get_realtime_quotes(codeList)
       zs = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
       queue.put({'df' : df,'zs' : zs})

   sched.start()