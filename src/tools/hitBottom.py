# -*-coding=utf-8-*-
__author__ = 'aqua'
import tushare as ts
import threading
import time
import pandas as pd
import sys
sys.path.append('..')
from config.Config import Config
from t1.datas.HitBottomDataHolder import HitBottomDataHolder
from t1.analyze.HitBottomAnalyze import HitBottomAnalyze
from t1.trade.MockTrade import MockTrade
from t1.MyLog import MyLog
from utils.Utils import Utils
from sqlalchemy import create_engine
import multiprocessing as mp
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

setting = Config()
mockTrade = MockTrade()
engine = create_engine(setting.get_DBurl())
analyze = HitBottomAnalyze()

def run(queue):
    MyLog.info('child process %s is running' % os.getpid())
    try:
        dh = None
        data = queue.get(True)
        while data is not None and data['df'] is not None and len(data['df']) > 0:
              timestamp = data['timestamp']
              df = data['df']
              if dh is None:
                 dh = HitBottomDataHolder() 
              dh.addData(df)
              res = analyze.calcMain(dh,timestamp)
              if len(res) > 0:
                 for code in res: 
                     dh.add_buyed(code)
              data = queue.get(True)   
    except Exception as e:
            MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   MyLog.info('main process %s.' % os.getpid()) 

   def init(forceUpdate):
       def cb(**kw):
           return ts.get_today_all()
       df_bottomAll = Utils.queryData('bottom_all','code',engine, cb, forceUpdate=forceUpdate)
       strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       while strTime < '14:30:00':
             time.sleep(0.1)
             strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       codeList = []
       for code in df_bottomAll['code'].tolist():
           codeList.append(code)
       return codeList

   pool = mp.Pool(setting.get_t1()['process_num'])
   manager = mp.Manager()

   codeLists = init(False)
   MyLog.info('calc stocks %s' % codeLists)
   codeSplitMaps = {} 
   queueMaps = {}
   interDataHolder = {
      'currentTime' : dt.datetime.now()
   }
   if setting.get_t1()['trade']['enableMock']:
      mockTrade.relogin() 
   for code in setting.get_ignore():
       if code in codeLists:
          codeLists.remove(code)  
   length = len(codeLists)
   MyLog.info('calc stocks size %d' % length) 
   if length == 0:
      MyLog.info('no available stocks to calc')
      sys.exit()
   step = setting.get_t1()['split_size']
   x = length // setting.get_t1()['process_num']
   y = length % setting.get_t1()['process_num']
   if x + y < setting.get_t1()['split_size']:
      step = x + y
   begin = 0
   less = 1
   if length % step == 0: 
      less = 0
   num_splits = length // step + less
   for i in range(num_splits):
       end = begin + step
       if end > length:
          end = length 
       code_split = codeLists[begin:end]
       codeSplitMaps[i] = code_split
       queue = manager.Queue()
       queueMaps[i] = queue
       pool.apply_async(run, (queue,))
       begin = end
       if begin >= length:
          break

   sched = BlockingScheduler()

   @sched.scheduled_job('interval', seconds=setting.get_t1()['get_data_inter'],max_instances=10)
   def getData():
       timestamp = dt.datetime.now()
       if setting.get_t1()['trade']['enableMock']:
          if (timestamp - interDataHolder['currentTime']).seconds > 60:
             interDataHolder['currentTime'] = timestamp
             mockTrade.relogin() 
       for key in codeSplitMaps:
           df = ts.get_realtime_quotes(codeSplitMaps[key])
           queueMaps[key].put({'timestamp' : timestamp,'df' : df})

   sched.start()
   pool.close()
   pool.join()