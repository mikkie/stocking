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
# from t1.analyze.Concept import Concept
# from t1.analyze.NetMoney import NetMoney
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
# thshy = pd.read_sql_table('thshy', con=engine)
# thsgn = pd.read_sql_table('concept', con=engine)
analyze = Analyze(None,None)
# concept = Concept()
# netMoney = NetMoney()

def run(queue):
        print('child process %s is running' % os.getpid())
        try:
            dh = None
            data = queue.get(True)
            while data is not None and data['df'] is not None and len(data['df']) > 0:
                  zs = data['zs']
                  df = data['df']
                  hygn = None
                  netMoney = None
                  s = int(round(time.time() * 1000))
                  if dh is None:
                     codeList = df['code'].tolist()
                     dh = DataHolder(codeList) 
                  dh.addData(df)
                  res = analyze.calcMain(zs,dh,hygn,netMoney)
                  if len(res) > 0:
                     for code in res: 
                         dh.add_buyed(code,True)
                  MyLog.debug('process %s, calc data time = %d' % (os.getpid(),(int(round(time.time() * 1000)) - s))) 
                  data = queue.get(True)   
        except Exception as e:
               MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   print('main process %s.' % os.getpid()) 

   def init(forceUpdate):
       def cb(**kw):
           return ts.get_today_all()
       df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=forceUpdate)
    #    df_todayAll = df_todayAll[df_todayAll.apply(analyze.isOpenMatch2, axis=1)]
    #    return df_todayAll['code'].tolist()
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
   print('calc stocks %s' % codeLists)
   codeSplitMaps = {} 
   queueMaps = {}
   interDataHolder = {
      'currentTime' : dt.datetime.now(),
      'hygn' : None,
      'netMoney' : None
   }
   mockTrade.relogin() 
   for code in setting.get_ignore():
       if code in codeLists:
          codeLists.remove(code)  
   length = len(codeLists)
   print('calc stocks size %d' % length) 
   if length == 0:
      print('no available stocks to calc')
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

   @sched.scheduled_job('interval', seconds=setting.get_t1()['get_data_inter'])
   def getData():
       now = dt.datetime.now()
       if (now - interDataHolder['currentTime']).seconds > 60:
          interDataHolder['currentTime'] = now
          mockTrade.relogin() 
        #   hygn = concept.getCurrentTopHYandConcept()
        #   if hygn is not None:
            #  interDataHolder['hygn'] = hygn 
        #   net = netMoney.getNetMoneyRatio()
        #   if netMoney is not None:
            #  interDataHolder['netMoney'] = net
       for key in codeSplitMaps:
           df = ts.get_realtime_quotes(codeSplitMaps[key])
           zs = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
           queueMaps[key].put({'zs' : zs,'df' : df,'hygn' : interDataHolder['hygn'],'netMoney' : interDataHolder['netMoney']})
        #    for debug     
        #    d = df[df['code'] == '300063']
        #    if d is not None and len(d) > 0:
        #       print('key=' + str(key))
        #       print('300063')

   sched.start()

   pool.close()
   pool.join()