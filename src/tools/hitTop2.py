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
              analyze.calcMain(zs,dh,timestamp,balance,lock)
              data = queue.get(True)   
    except Exception as e:
           MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   MyLog.info('main process %s.' % os.getpid()) 
   engine = create_engine(setting.get_DBurl()) 
   mockTrade = MockTrade()
   if setting.get_t1()['trade']['enable']:
      trade = Trade()

   def init(forceUpdate):
       def cb(**kw):
           df = ts.get_today_all()
           df['pick'] = 0
           return df
       df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=forceUpdate, sql='select * from today_all where pick = 1', load_if_empty=False)
       strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       while strTime < '09:30:01':
             time.sleep(0.1)
             strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       step = 880
       start = 0
       codeList = []
       length = len(df_todayAll)
       if length == 0:
          MyLog.info('no stocks to calc')
          return 
       origin_code_list = df_todayAll['code'].tolist()
       
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
       return (origin_code_list, codeList)

   pool = mp.Pool(setting.get_t1()['process_num'])
   manager = mp.Manager()
   lock = manager.Lock()
   balance = manager.Value('i',setting.get_t1()['trade']['balance'])

   old_code_list, codeLists = init(False)

   calc_stock_size = len(codeLists) 
   x = calc_stock_size // setting.get_t1()['split_size']
   y = calc_stock_size % setting.get_t1()['split_size']
   process_size = x + (1 if y != 0 else 0)
   proxy_size = math.ceil(process_size * 1.5)
   proxyManager = ProxyManager(proxy_size)

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

   @sched.scheduled_job('interval', seconds=setting.get_t1()['eyes_on_codes_change'],max_instances=10)
   def eyes_on_codes_change(): 
       global old_code_list   
       global num_splits
       def cb(**kw):
           df = ts.get_today_all()
           df['pick'] = 0
           return df
       new_df = Utils.queryData('today_all','code',engine, cb, forceUpdate=False, sql='select * from today_all where pick = 1', load_if_empty=False) 
       if len(new_df) == 0:
          return
       new_code_list = new_df['code'].tolist() 
       old_code_list.sort()
       new_code_list.sort()
       add = []
       delete = []
       for n_code in new_code_list:
           if n_code not in old_code_list:
              add.append(n_code)
       for o_code in old_code_list:
           if o_code not in new_code_list:
              delete.append(o_code)
       old_code_list = new_code_list       
       for code in delete:
           for key in codeSplitMaps:
               if code in codeSplitMaps[key]:
                  codeSplitMaps[key].remove(code)
                  break
       length = len(add)
       if length == 0:
          return 
       x = length // 100
       y = length % 100
       size = x + (1 if y != 0 else 0)
       begin = 0
       step = setting.get_t1()['split_size']
       for i in range(size):
           end = begin + step
           if end > length:
              end = length
           code_list = add[begin:end]
           codeSplitMaps[num_splits] = code_list
           queue = manager.Queue()
           queueMaps[num_splits] = queue
           pool.apply_async(run, args=(queue,balance,lock))
           MyLog.info('calc new added stocks %s' % code_list)
           num_splits = num_splits + 1
           begin = end
           if begin >= length:
              break
       proxyManager.append_proxy(size)     






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
          if delBalanceSeconds > 320:
             interDataHolder['balanceTime'] = timestamp 
             try:
                lock.acquire()
                trade.refresh()
                balance = trade.queryBalance()
                if balance is not None:
                   interDataHolder['balance'] = balance  
             except Exception as e:
                    interDataHolder['balance'] = None 
             finally:    
                    lock.release() 
          if delQueryBuySeconds > 350:
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
   try:
       trade.refresh()
   except Exception as e:
          pass    
   sched.start()
   pool.close()
   pool.join()