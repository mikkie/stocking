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


def isInTradingTime():
    now = dt.datetime.now()
    return (now > dt.datetime(now.year,now.month,now.day,9,30) and now < dt.datetime(now.year,now.month,now.day,11,30)) or (now > dt.datetime(now.year,now.month,now.day,13,0) and now < dt.datetime(now.year,now.month,now.day,15,0))

def getData(setting):
    df_hist_km5 = pd.read_sql_table('km5', con=engine)
    df_hist_kd3 = pd.read_sql_table('kd3', con=engine)
    return df_hist_km5,df_hist_kd3

def initData(setting):
    df_todayAll = ts.get_today_all()
    priceRange = setting.get_PriceRange()
    return df_todayAll[(df_todayAll['trade'] >= priceRange['min']) & (df_todayAll['trade'] <= priceRange['max'])]



def filterSuperSoldIn3Months(df_todayAll):
    result = [];
    now = dt.datetime.now()
    timeDelta = dt.timedelta(30 * 3)
    threeMbefore = (now - timeDelta).strftime('%Y-%m-%d')
    for index,row in df_todayAll.iterrows():
        code = row['code']
        df_3m = ts.get_hist_data(code,start=threeMbefore,ktype='M')
        if df_3m.empty:
           continue 
        high = df_3m.loc[df_3m['high'].idxmax()].get('high')
        low = df_3m.loc[df_3m['low'].idxmin()].get('low')
        avgClose = df_3m['close'].mean()
        close = df_3m.iloc[0].get('close')
        if np.isnan(high) or np.isnan(low) or np.isnan(avgClose) or np.isnan(close):
           continue 
        ratio = (close - low) / (high - low)
        if (high - low) / avgClose > setting.get_pKM3Change() and ratio < setting.get_SuperSold()[1] and ratio > setting.get_SuperSold()[0]:
            # print(code)
            result.append(code)
    return result        

#setting
setting = conf.Config()
engine = create_engine(setting.get_DBurl())
df_stocksPool = None
if isInTradingTime() and len(sys.argv) == 1:
   #交易监控 
   #data
   data_km5,data_kd3 = getData(setting)
   #strategy
   dad = ds.DadStrategy()
   #run
   dad.chooseStock({'km5' : data_km5,'kd3' : data_kd3},setting)
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
      result = filterSuperSoldIn3Months(df_stocks)
      df_code = pd.DataFrame(np.array(result).reshape(len(result),1), columns = ['code'])
      df_code.to_sql('codes',con=engine,if_exists='replace',index=False,index_label='code')





