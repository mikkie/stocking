# -*-coding=utf-8-*-

__author__ = 'aqua'

import sys
import pandas as pd
import numpy as np
import tushare as ts
import handlers.DadStrategy as ds
import config.Config as conf
from sqlalchemy import create_engine
import datetime as dt
import time
import handlers.filters.quarterFilter as qf
import threading


def isInTradingTime():
    now = dt.datetime.now()
    return (now > dt.datetime(now.year,now.month,now.day,9,30) and now < dt.datetime(now.year,now.month,now.day,11,30)) or (now > dt.datetime(now.year,now.month,now.day,13,0) and now < dt.datetime(now.year,now.month,now.day,15,0))

def getData():
    df_codes = pd.read_sql_table('codes', con=engine)
    return df_codes

def initData(setting):
    df_todayAll = ts.get_today_all()
    priceRange = setting.get_PriceRange()
    return df_todayAll[(df_todayAll['trade'] >= priceRange['min']) & (df_todayAll['trade'] <= priceRange['max']) & (df_todayAll['p_change'] >= 1.00)]

#setting
setting = conf.Config()
engine = create_engine(setting.get_DBurl())
df_stocksPool = None

def runEachMin(df_codes,dad):
    print('正在监控==== ', dt.datetime.now())
    for index,row in df_codes.iterrows():
        code = row['code']
        now = dt.datetime.now()
        start = dt.datetime(now.year,now.month,now.day,9,30).strftime('%Y-%m-%d')
        df_5m = ts.get_hist_data(code,start=start, ktype='5')
        df_5m = df_5m[::-1]
        #run
        if dad.chooseStock(df_5m,setting):
           print(code)
    timer = threading.Timer(60, runEachMin,[df_codes,dad])
    timer.start()       


if (isInTradingTime() and len(sys.argv) == 1) or (len(sys.argv) == 2 and str(sys.argv[1]) == 'start'):
   #交易监控 
   #data
   df_codes = getData()
   #strategy
   dad = ds.DadStrategy()
   timer = threading.Timer(60, runEachMin,[df_codes,dad])
   timer.start()

   while True:
         time.sleep(0.5)
   pass 
else:
   #初始化数据 
   if len(sys.argv) >= 2 and str(sys.argv[1]) == 'init':
      if len(sys.argv) == 3 and str(sys.argv[2]) == '0':
         print('=====执行价格过滤=====',setting.get_PriceRange())  
         df_stocksPool = initData(setting) 
         df_stocksPool = df_stocksPool.sort_values('trade')
         df_stocksPool.to_sql('stocks',con=engine,if_exists='replace',index=False,index_label='code')
         print(df_stocksPool)
      df_stocks = pd.read_sql_table('stocks', con=engine)
      result = qf.filterSuperSoldIn3Months(df_stocks,setting)
    #   df_code = pd.DataFrame(np.array(result).reshape(len(result),1), columns = ['code'])
    #   df_code.to_sql('codes',con=engine,if_exists='replace',index=False,index_label='code')
      df_codes =  df_stocks[df_stocks.index.map(lambda x : x in result)]
      df_codes.to_sql('codes',con=engine,if_exists='replace',index=False,index_label='code')





