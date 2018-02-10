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
                     dh = DataHolder(codeList) 
                  dh.addData(df)
                  res = analyze.calcMain(dh)
                  if res != '':
                     dh.add_buyed(res,True)
                  MyLog.debug('process %s, calc data time = %d' % (os.getpid(),(int(round(time.time() * 1000)) - s))) 
                  df = queue.get(True)   
        except Exception as e:
               MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   print('main process %s.' % os.getpid()) 

   def init(forceUpdate):
       def cb(**kw):
           return ts.get_today_all()
       df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=forceUpdate)
       strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       while strTime < '09:30:01':
             time.sleep(0.1)
             strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       step = setting.get_t1()['split_size']
       start = 0
       codeList = []
       length = len(df_todayAll)
       while start < length:
             end = start + step
             if end >= length:
                end = length 
             df_temp = df_todayAll.iloc[start:end]
             df = ts.get_realtime_quotes(df_temp['code'].tolist())
             df = df[df.apply(analyze.isOpenMatch, axis=1)]
             for code in df['code'].tolist():
                 codeList.append(code)
             start = end
       return codeList

   pool = mp.Pool(setting.get_t1()['process_num'])
   manager = mp.Manager()

   codeLists = init(False)
#    codeLists = ['300063']
   codeSplitMaps = {} 
   queueMaps = {}

   for code in setting.get_ignore():
       if code in codeLists:
          codeLists.remove(code)  
   length = len(codeLists)
   print('calc stocks size %d' % length) 
   begin = 0
   less = 1
   if length % setting.get_t1()['split_size'] == 0: 
      less = 0
   num_splits = length // setting.get_t1()['split_size'] + less
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
        #    d = df[df['code'] == '300063']
        #    if d is not None and len(d) > 0:
        #       print('key=' + str(key))
        #       print('300063')

   sched.start()
   pool.close()
   pool.join()
else:
    print('child process %s is running' % os.getpid())     