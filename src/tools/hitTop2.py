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
import math
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

setting = Config()
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
              if data['balance'] is not None:
                 balance.value = data['balance']
              if dh is None:
                 dh = NewDataHolder2() 
              dh.addData(df)
              print(df)
              analyze.calcMain(zs,dh,timestamp,balance,lock)
              data = queue.get(True)   
    except Exception as e:
           MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   MyLog.info('main process %s.' % os.getpid()) 

   mockTrade = MockTrade()
   if setting.get_t1()['trade']['enable']:
      trade = Trade()

   def init(forceUpdate):
       def cb(**kw):
           return ts.get_today_all()
       engine = create_engine(setting.get_DBurl()) 
       df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=forceUpdate)
       strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
    #    while strTime < '09:30:01':
    #          time.sleep(0.1)
    #          strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       step = 880
       start = 0
       codeList = []
       length = len(df_todayAll)
       proxy_size = math.ceil(length // setting.get_t1()['split_size'] * 1.5)
       proxyManager = ProxyManager(proxy_size)
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
       return codeList, proxyManager

   pool = mp.Pool(setting.get_t1()['process_num'])
   manager = mp.Manager()
   lock = manager.Lock()
   balance = manager.Value('i',setting.get_t1()['trade']['balance'])

   codeLists, proxyManager = init(False)
   MyLog.info('calc stocks %s' % codeLists)
   codeSplitMaps = {} 
   queueMaps = {}
   now_temp = dt.datetime.now() 
   interDataHolder = {
      'currentTime' : now_temp,
      'balanceTime' : now_temp,
      'queryBuyTime' : now_temp,
      'stopBuy' : False,
      'zs' : None,
      'balance' : None
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
      os._exit(0)
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

   def put_data_to_queue(df,queue,data):
       data['df'] = df
       queue.put(data)


   @sched.scheduled_job('interval', seconds=setting.get_t1()['get_data_inter'],max_instances=10)
   def getData():
       timestamp = dt.datetime.now()
       if setting.get_t1()['trade']['enableMock']:
          delSeconds = (timestamp - interDataHolder['currentTime']).seconds
          delQueryBuySeconds = (timestamp - interDataHolder['queryBuyTime']).seconds
          if delSeconds > 30:
             interDataHolder['currentTime'] = timestamp
             interDataHolder['zs'] = proxyManager.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'],batch_size=0,use_proxy_no_batch=True)
          if delQueryBuySeconds > 120:
             interDataHolder['queryBuyTime'] = timestamp 
             mockTrade.relogin() 
             count = mockTrade.queryBuyStocks()
             if count >= setting.get_t1()['trade']['max_buyed']:
                mockTrade.cancelAllBuy()
                MyLog.info('buyed 3 stocks')
                interDataHolder['stopBuy'] = True 
       if setting.get_t1()['trade']['enable']: 
          delSeconds = (timestamp - interDataHolder['currentTime']).seconds
          delBalanceSeconds = (timestamp - interDataHolder['balanceTime']).seconds
          delQueryBuySeconds = (timestamp - interDataHolder['queryBuyTime']).seconds
          if delSeconds > 30:
              interDataHolder['currentTime'] = timestamp
              interDataHolder['zs'] = proxyManager.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'],batch_size=0,use_proxy_no_batch=True)
          if delBalanceSeconds > 70:
             interDataHolder['balanceTime'] = timestamp 
             try:
                lock.acquire()
                balance = trade.queryBalance()
                if balance is not None:
                   interDataHolder['balance'] = balance  
             except Exception as e:
                    interDataHolder['balance'] = None 
             finally:    
                    lock.release() 
          if delQueryBuySeconds > 120:
             interDataHolder['queryBuyTime'] = timestamp 
             try:
                lock.acquire()
                count = trade.queryBuyStocks()
                if count >= setting.get_t1()['trade']['max_buyed']:
                   trade.cancel(None,True) 
                   MyLog.info('buyed 3 stocks')
                   interDataHolder['stopBuy'] = True  
             except Exception as e:
                    pass 
             finally:    
                    lock.release()
       if interDataHolder['stopBuy']:
          os._exit(0)
          return 
       if interDataHolder['zs'] is None:
          interDataHolder['zs'] = proxyManager.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'],batch_size=0,use_proxy_no_batch=True)   
       for key in codeSplitMaps:
           df = proxyManager.get_realtime_quotes(codeSplitMaps[key],queueMaps[key],{'timestamp' : timestamp,'df' : None,'zs' : interDataHolder['zs'], 'balance' : interDataHolder['balance']},batch_size=100,async_exe=put_data_to_queue)

   getData()
   sched.start()
   pool.close()
   pool.join()