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
import multiprocessing as mp
import os
from apscheduler.schedulers.blocking import BlockingScheduler

setting = Config()
engine = create_engine(setting.get_DBurl())
analyze = Analyze()

def run(queue):
        try:
            dh = None
            df = queue.get(True)
            while df is not None and len(df) > 0:
                  s = int(round(time.time() * 1000))
                  if dh is None:
                     codeList = df['code'].tolist()
                     dh = DataHolder(codeList,False) 
                  dh.addData(df)
                  res = analyze.calcMain(dh)
                  if res != '':
                     dh.add_buyed(res)
                  MyLog.debug('process %s, calc data time = %d' % (os.getpid(),(int(round(time.time() * 1000)) - s))) 
                  df = queue.get(True)     
        except Exception as e:
               MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   MyLog.debug('main process %s.' % os.getpid()) 

   def init(forceUpdate):
       def cb(**kw):
           return ts.get_today_all()
       df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=forceUpdate)
       df_todayAll = df_todayAll[df_todayAll['changepercent'] >= -1.0]
       return df_todayAll['code']

   pool = mp.Pool(setting.get_t1()['process_num'])
   manager = mp.Manager()

   codes = init(False)
   codeLists = codes.tolist()
   codeSplitMaps = {} 
   queueMaps = {}

   for code in setting.get_ignore():
       if code in codeLists:
          codeLists.remove(code)  
   length = len(codeLists)
   begin = 0
   num_splits = length // setting.get_t1()['split_size'] + 1
   for i in range(num_splits):
       end = begin + setting.get_t1()['split_size']
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

   @sched.scheduled_job('interval', seconds=setting.get_t1()['get_data_inter'])
   def getData():
       for key in codeSplitMaps:
           df = ts.get_realtime_quotes(codeSplitMaps[key])
           queueMaps[key].put(df)
        #    for debug     
        #    d = df[df['code'] == '002460']
        #    if d is not None and len(d) > 0:
        #       print(d.iloc[0]['time'])

   sched.start()
   pool.close()
   pool.join()
else:
    MyLog.debug('child process %s is running' % os.getpid())     