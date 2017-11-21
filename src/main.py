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
    if str(sys.argv[2]) == '50': #上证50成份股
         sz50CodeList = getSZ50CodeList() 
         df_todayAll = df_todayAll[df_todayAll['code'].isin(sz50CodeList)]
    elif str(sys.argv[2]) == '300':  #沪深50成份股
         hs300CodeList = getHS300CodeList() 
         df_todayAll = df_todayAll[df_todayAll['code'].isin(hs300CodeList)]
    elif str(sys.argv[2]) == 'zx':  #中小盘
         zxCodeList = getZXCodeList() 
         df_todayAll = df_todayAll[df_todayAll['code'].isin(zxCodeList)]           
    if len(sys.argv) > 4:
       if str(sys.argv[3]) == 'hy':  #行业分类
            hyCodeList = getHYCodeList()    
            df_todayAll = df_todayAll[df_todayAll['code'].isin(hyCodeList)]
       elif str(sys.argv[3]) == 'c':  #概念分类
            cCodeList = getConceptCodeList()    
            df_todayAll = df_todayAll[df_todayAll['code'].isin(cCodeList)]      
    return df_todayAll[(df_todayAll['trade'] >= priceRange['min']) & (df_todayAll['trade'] <= priceRange['max']) & (df_todayAll['turnoverratio'] > setting.get_TurnOver())]

#获取上证50代码列表
def getSZ50CodeList():
    df_sz50 = ts.get_sz50s()
    return df_sz50['code'].tolist()

#获取沪深300代码列表
def getHS300CodeList():
    df_hs300 = ts.get_hs300s()
    return df_hs300['code'].tolist()

#获取中小板代码列表
def getZXCodeList():
    df_zx = ts.get_sme_classified()
    return df_zx['code'].tolist()

#获取行业股票代码
def getHYCodeList():
    if len(sys.argv) < 5:
       raise Exception('缺少参数:行业名称')
    hyName = str(sys.argv[4])
    df_hy = ts.get_industry_classified()
    df_hy = df_hy.loc[df_hy['c_name'] == hyName]
    return df_hy['code'].tolist()

#获取概念股票代码
def getConceptCodeList():
    if len(sys.argv) < 5:
           raise Exception('缺少参数:概念名称')
    cName = str(sys.argv[4])
    df_c = ts.get_concept_classified()
    df_c = df_c.loc[df_c['c_name'] == cName]
    return df_c['code'].tolist()


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
      if len(sys.argv) >= 3 and (str(sys.argv[2]) == '0' or str(sys.argv[2]) == '50' or str(sys.argv[2]) == '300' or str(sys.argv[2]) == 'zx' or str(sys.argv[2]) == 'hy' or str(sys.argv[2]) == 'c'):
         print('=====执行价格,换手率过滤=====',setting.get_PriceRange())  
         df_stocksPool = initData(setting) 
         df_stocksPool = df_stocksPool.sort_values('trade')
         df_stocksPool.to_sql('stocks',con=engine,if_exists='replace',index=False,index_label='code')
         print(df_stocksPool)
      df_stocks = pd.read_sql_table('stocks', con=engine)
      result = qf.filterSuperSoldIn3Months(df_stocks,setting)
    #   df_code = pd.DataFrame(np.array(result).reshape(len(result),1), columns = ['code'])
    #   df_code.to_sql('codes',con=engine,if_exists='replace',index=False,index_label='code')
      df_codes = df_stocks[df_stocks.code.isin(result)]
      df_codes = df_codes.sort_values('changepercent',ascending=False)
      df_codes.to_sql('codes',con=engine,if_exists='replace',index=False,index_label='code')




