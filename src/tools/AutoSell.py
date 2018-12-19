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
from t1.trade.trade import Trade
from t1.trade.MockTrade import MockTrade
from t1.trade.ProxyManager import ProxyManager
from t1.MyLog import MyLog
from utils.Utils import Utils
from sqlalchemy import create_engine
import multiprocessing as mp
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

codeList = ['002089','002229','300588']
setting = Config()
mockTrade = MockTrade()
engine = create_engine(setting.get_DBurl())
analyze = SellAnalyze()


def run(queue, balance):
    MyLog.info('child process %s is running' % os.getpid())
    try:
        dh = None
        data = queue.get(True)
        while data is not None and data['df'] is not None and len(data['df']) > 0:
            df = data['df']
            zs = data['zs']
            if data['balance'] is not None:
               balance.value = data['balance']
            s = int(round(time.time() * 1000))
            if dh is None:
               codeList = df['code'].tolist()
               dh = DataHolder(codeList) 
            dh.addSellData(df)
            analyze.calcMain(zs,dh,balance)
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
   if setting.get_t1()['trade']['enable']:
      trade = Trade(isSell=True)   
   pool = mp.Pool(1)
   manager = mp.Manager()
   queue = manager.Queue()
   balance = manager.Value('i',setting.get_t1()['trade']['balance'])
   pool.apply_async(run, (queue,balance))
   sched = BlockingScheduler()
   interDataHolder = {
      'currentTime' : dt.datetime.now(),
      'balance' : None
   }
   proxyManager = ProxyManager(2)

   @sched.scheduled_job('interval', seconds=setting.get_t1()['get_data_inter'])
   def getData():
       strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       if strTime > '11:30:30' and strTime < '12:59:30': 
          return
       if strTime > '15:30:30':
          os._exit(0)
          return
       if setting.get_t1()['trade']['enableMock']:
          now = dt.datetime.now()
          if (now - interDataHolder['currentTime']).seconds > 60:
             interDataHolder['currentTime'] = now
             mockTrade.relogin()
       if setting.get_t1()['trade']['enable']:
          now = dt.datetime.now()
          if (now - interDataHolder['currentTime']).seconds > 320:
             interDataHolder['currentTime'] = now
             trade.refresh() 
             interDataHolder['balance'] = trade.queryBalance()  
       df = proxyManager.get_realtime_quotes(codeList,batch_size=0,use_proxy_no_batch=True)
       zs = proxyManager.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'],batch_size=0,use_proxy_no_batch=True)
       queue.put({'df' : df,'zs' : zs, 'balance' : interDataHolder['balance']})

   sched.start()