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
from multiprocessing import Pool, Queue
import os

setting = Config()
engine = create_engine(setting.get_DBurl())
analyze = Analyze()


def get_today_all_codes():
    def cb(**kw):
        return ts.get_today_all()
    df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=False)
    df_todayAll = df_todayAll[df_todayAll['changepercent'] >= -1.0]
    return df_todayAll['code']

def run(codeList,dh):
    try:
        s = int(round(time.time() * 1000))
        if dh is None:
           dh = DataHolder(codeList) 
        now = time.strftime('%H:%M:%S',time.localtime(time.time()))
        if (now >= setting.get_t1()['stop']['am_start'] and now <= setting.get_t1()['stop']['am_stop']) or (now >= setting.get_t1()['stop']['pm_start'] and now <= setting.get_t1()['stop']['pm_stop']): 
           if len(dh.get_buyed()) > 0:
              for code in dh.get_buyed():
                  if code in codeList:
                     codeList.remove(code)
           if len(codeList) > 0: 
              df = ts.get_realtime_quotes(codeList)
           if len(df) > 0:
            #   a = int(round(time.time() * 1000)) 
              dh.addData(df)
            #   b = int(round(time.time() * 1000))
            #   print('process %s, add data time = %d' % (os.getpid(),(b - a)))
              res = analyze.calcMain(dh)
            #   print('process %s, calc data time = %d' % (os.getpid(),(int(round(time.time() * 1000)) - b)))
              if res != '':
                 dh.add_buyed(res)
    except Exception as e:
           MyLog.error('error %s' % str(e))
    finally: 
           now = time.strftime('%H:%M:%S',time.localtime(time.time()))
           if now < setting.get_t1()['stop']['pm_stop']:                
              global timer
              timer = threading.Timer(0, run, args=[codeList,dh])
              timer.start()
              e = int(round(time.time() * 1000))
              print('process %s, run once time = %d' % (os.getpid(),(e - s)))

if __name__ == '__main__':
   print('main process %s.' % os.getpid()) 
   pool = Pool(setting.get_t1()['process_num'])
   codes = get_today_all_codes()
   codeLists = codes.tolist()
#    codeLists = ['002496','600516','600158','002460','002466','000426']
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
       pool.apply_async(run, args=(code_split,None))
       begin = end
       if begin >= length:
          break
   pool.close()
   pool.join()
else:
    print('process %s is running' % os.getpid())     
