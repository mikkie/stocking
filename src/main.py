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
from utils.Utils import Utils



def isInTradingTime():
    now = dt.datetime.now()
    return (now > dt.datetime(now.year,now.month,now.day,9,30) and now < dt.datetime(now.year,now.month,now.day,11,30)) or (now > dt.datetime(now.year,now.month,now.day,13,0) and now < dt.datetime(now.year,now.month,now.day,15,0))

def getData():
    df_codes = pd.read_sql_table('codes', con=engine)
    return df_codes

def initData(setting):
    def cb(**kw):
        return ts.get_today_all()
    df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=False)
    priceRange = setting.get_PriceRange()
    if str(sys.argv[2]) == '1': #test
         specificList = getSpecificCode(setting)
         df_todayAll = df_todayAll[df_todayAll['code'].isin(specificList)]
    if str(sys.argv[2]) == '300': #上证50成份股
         sz50CodeList = getSZ50CodeList() 
         df_todayAll = df_todayAll[df_todayAll['code'].isin(sz50CodeList)]
    elif str(sys.argv[2]) == '300':  #沪深50成份股
         hs300CodeList = getHS300CodeList() 
         df_todayAll = df_todayAll[df_todayAll['code'].isin(hs300CodeList)]
    elif str(sys.argv[2]) == 'zx':  #中小盘
         zxCodeList = getZXCodeList() 
         df_todayAll = df_todayAll[df_todayAll['code'].isin(zxCodeList)] 
    elif str(sys.argv[2]) == 'cy':  #创业板 
         cyCodeList = getCYCodeList() 
         df_todayAll = df_todayAll[df_todayAll['code'].isin(cyCodeList)]
    elif str(sys.argv[2]) == 'zz':  #中证500
         zzCodeList = getZZCodeList()
         df_todayAll = df_todayAll[df_todayAll['code'].isin(zzCodeList)]
    elif str(sys.argv[2]) == 'tiger': #龙虎榜
         tigerList = getTigerCodeList()
         df_todayAll = df_todayAll[df_todayAll['code'].isin(tigerList)]
         pass             
    if len(sys.argv) > 4:
       if str(sys.argv[3]) == 'hy':  #行业分类
            hyCodeList = getHYCodeList()    
            df_todayAll = df_todayAll[df_todayAll['code'].isin(hyCodeList)]
       elif str(sys.argv[3]) == 'c':  #概念分类
            cCodeList = getConceptCodeList()    
            df_todayAll = df_todayAll[df_todayAll['code'].isin(cCodeList)]      
    return df_todayAll[(df_todayAll['trade'] >= priceRange['min']) & (df_todayAll['trade'] <= priceRange['max'])]


def getSpecificCode(setting):
    return setting.get_TestCodes()

#获取上证50代码列表
def getSZ50CodeList():
    df_sz50 = None
    try:
        df_sz50 = pd.read_sql_table('sz50', con=engine)
    except:
        pass
    if df_sz50 is None or df_sz50.empty:
       df_sz50 = ts.get_sz50s()
       df_sz50.to_sql('sz50',con=engine,if_exists='replace',index=False,index_label='code')
    return df_sz50['code'].tolist()

#获取沪深300代码列表
def getHS300CodeList():
    df_hs300 = None
    try:
        df_hs300 = pd.read_sql_table('hs300', con=engine)
    except:
        pass
    if df_hs300 is None or df_hs300.empty:
       df_hs300 = ts.get_hs300s()
       df_hs300.to_sql('hs300',con=engine,if_exists='replace',index=False,index_label='code')
    return df_hs300['code'].tolist()

#获取中小板代码列表
def getZXCodeList():
    df_zx = None
    try:
        df_zx = pd.read_sql_table('zx', con=engine)
    except:
        pass
    if df_zx is None or df_zx.empty:
       df_zx = ts.get_sme_classified()
       df_zx.to_sql('zx',con=engine,if_exists='replace',index=False,index_label='code')
    return df_zx['code'].tolist()

#获取龙虎榜
def getTigerCodeList():
    def cb(**kw):
        return ts.inst_tops()
    df_tiger = Utils.queryData('tiger','code',engine, cb, forceUpdate=True)
    df_tiger = df_tiger[df_tiger['net'] > 0]
    return df_tiger['code'].tolist()

#获取创业榜
def getCYCodeList():
    df_cy = None
    try:
       df_cy = pd.read_sql_table('cy', con=engine)
    except:
        pass
    if df_cy is None or df_cy.empty:
       df_cy = ts.get_gem_classified()
       df_cy.to_sql('cy',con=engine,if_exists='replace',index=False,index_label='code')
    return df_cy['code'].tolist()


#获取中证500列表
def getZZCodeList():
    df_zz = None
    try:
       df_zz = pd.read_sql_table('zz', con=engine)
    except:
        pass
    if df_zz is None or df_zz.empty:
       df_zz = ts.get_zz500s()
       df_zz.to_sql('zz',con=engine,if_exists='replace',index=False,index_label='code')
    return df_zz['code'].tolist()



#获取行业股票代码
def getHYCodeList():
    if len(sys.argv) < 5:
       raise Exception('缺少参数:行业名称')
    hyName = str(sys.argv[4])
    df_hy = None
    try:
        df_hy = pd.read_sql_table('hy', con=engine)
    except:
        pass
    if df_hy is None or df_hy.empty:
       df_hy = ts.get_industry_classified()
       df_hy.to_sql('hy',con=engine,if_exists='replace',index=False,index_label='code')
    df_hy = df_hy.loc[df_hy['c_name'].str.contains(hyName)]
    return df_hy['code'].tolist()

#获取概念股票代码
def getConceptCodeList():
    if len(sys.argv) < 5:
           raise Exception('缺少参数:概念名称')
    cName = str(sys.argv[4])
    df_c = None
    try:
        df_c = pd.read_sql_table('c', con=engine)
    except:
        pass
    if df_c is None or df_c.empty:
       df_c = ts.get_concept_classified()
       df_c.to_sql('c',con=engine,if_exists='replace',index=False,index_label='code')
    df_c = df_c.loc[df_c['c_name'].str.contains(cName)]
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
      if len(sys.argv) >= 3 and (str(sys.argv[2]) == '0' or str(sys.argv[2]) == '1' or str(sys.argv[2]) == '50' or str(sys.argv[2]) == '300' or str(sys.argv[2]) == 'zx' or str(sys.argv[2]) == 'hy' or str(sys.argv[2]) == 'c' or str(sys.argv[2]) == 'tiger' or str(sys.argv[2]) == 'cy' or str(sys.argv[2]) == 'zz'):
         print('=====执行基础过滤=====')  
         df_stocksPool = initData(setting) 
         df_stocksPool = df_stocksPool.sort_values('trade')
         df_stocksPool.to_sql('stocks',con=engine,if_exists='replace',index=False,index_label='code')
        #  print(df_stocksPool)
      df_stocks = pd.read_sql_table('stocks', con=engine)
      result = qf.filter(df_stocks,setting, engine)
    #   df_code = pd.DataFrame(np.array(result).reshape(len(result),1), columns = ['code'])
    #   df_code.to_sql('codes',con=engine,if_exists='replace',index=False,index_label='code')
      df_codes = df_stocks[df_stocks.code.isin(result)]
      df_codes = df_codes.sort_values('changepercent',ascending=False)
    #   print(df_codes)
      df_codes.to_sql('codes',con=engine,if_exists='replace',index=False,index_label='code')




