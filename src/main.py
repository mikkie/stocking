# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd
import tushare as ts
import handlers.DadStrategy as ds
import config.Config as conf
from sqlalchemy import create_engine
from datetime import datetime


def isInTradingTime():
    now = datetime.now()
    return (now > datetime(now.year,now.month,now.day,9,30) and now < datetime(now.year,now.month,now.day,11,30)) or (now > datetime(now.year,now.month,now.day,13,0) and now < datetime(now.year,now.month,now.day,15,0))

def getData(setting):
    df_hist_km5 = pd.read_sql_table('km5', con=engine)
    df_hist_kd3 = pd.read_sql_table('kd3', con=engine)
    return df_hist_km5,df_hist_kd3

def initData(setting):
    df_todayAll = ts.get_today_all()
    priceRange = setting.get_PriceRange()
    for index in df_todayAll.index:
        price = df_todayAll.loc[index].get('trade')
        if price >= priceRange['min'] and price <= priceRange['max']:
           print('价格匹配',price)  
    pass


#setting
setting = conf.Config()
engine = create_engine(setting.get_DBurl())
if isInTradingTime():
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
   initData(setting) 
   pass    





