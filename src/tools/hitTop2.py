# -*-coding=utf-8-*-
__author__ = 'aqua'
import tushare as ts
import threading
import time
import pandas as pd
import sys
sys.path.append('..')
from config.Config import Config
from t1.datas.NewDataHolder2 import NewDataHolder2
from t1.analyze.NewAnalyze2 import NewAnalyze2
from t1.trade.MockTrade import MockTrade
from t1.trade.trade import Trade
from t1.trade.ProxyManager import ProxyManager
from t1.MyLog import MyLog
from utils.Utils import Utils
from sqlalchemy import create_engine
import multiprocessing as mp
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

setting = Config()
proxyManager = ProxyManager()
mockTrade = MockTrade()
if setting.get_t1()['trade']['enable']:
   trade = Trade()
engine = create_engine(setting.get_DBurl())
analyze = NewAnalyze2()

def run(queue,balance,lock):
    MyLog.info('child process %s is running' % os.getpid())
    try:
        dh = None
        data = queue.get(True)
        while data is not None and data['df'] is not None and len(data['df']) > 0:
              timestamp = data['timestamp']
              df = data['df']
              zs = data['zs']
              if dh is None:
                 dh = NewDataHolder2() 
              dh.addData(df)
              analyze.calcMain(zs,dh,timestamp,balance,lock)
              data = queue.get(True)   
    except Exception as e:
           MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   MyLog.info('main process %s.' % os.getpid()) 

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
   lock = manager.Lock()
   balance = manager.Value('i',setting.get_t1()['trade']['balance'])

   codeLists = init(False)
   MyLog.info('calc stocks %s' % codeLists)
   codeSplitMaps = {} 
   queueMaps = {}
   interDataHolder = {
      'currentTime' : dt.datetime.now(),
      'stopBuy' : False,
      'zs' : None
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
       pool.apply_async(run, args=(queue,balance,lock))
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
             interDataHolder['zs'] = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'],add_proxy=proxyManager.add_proxy,remove_proxy=proxyManager.move_to_backup)
             mockTrade.relogin() 
             count = mockTrade.queryBuyStocks()
             if count >= setting.get_t1()['trade']['max_buyed']:
                mockTrade.cancelAllBuy()
                MyLog.info('buyed 3 stocks')
                interDataHolder['stopBuy'] = True 
       if setting.get_t1()['trade']['enable']: 
          if (timestamp - interDataHolder['currentTime']).seconds > 60:
              interDataHolder['currentTime'] = timestamp
              interDataHolder['zs'] = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'],add_proxy=proxyManager.add_proxy,remove_proxy=proxyManager.move_to_backup)
              count = trade.queryBuyStocks()
              if count >= setting.get_t1()['trade']['max_buyed']:
                 try:
                    lock.acquire()
                    trade.cancel(None,True) 
                 except Exception as e:
                        pass 
                 finally:    
                        lock.release()
                 MyLog.info('buyed 3 stocks')
                 interDataHolder['stopBuy'] = True  
       if interDataHolder['stopBuy']:
          os._exit(0)
          return 
       if interDataHolder['zs'] is None:
          interDataHolder['zs'] = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'],add_proxy=proxyManager.add_proxy,remove_proxy=proxyManager.move_to_backup)   
       for key in codeSplitMaps:
           df = ts.get_realtime_quotes(codeSplitMaps[key],add_proxy=proxyManager.add_proxy,remove_proxy=proxyManager.move_to_backup)
           queueMaps[key].put({'timestamp' : timestamp,'df' : df,'zs' : interDataHolder['zs']})

   sched.start()
   pool.close()
   pool.join()