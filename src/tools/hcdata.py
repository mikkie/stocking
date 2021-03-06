# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import os
import pandas as pd
import re
from datetime import timedelta
import datetime as dt
from sqlalchemy import create_engine
import sys
sys.path.append('..')
from utils.Utils import Utils

engine = create_engine('mysql://root:aqua@127.0.0.1/stocking?charset=utf8')


def re_build_data(df, code, date, pre_close, save):
    df['pre_close'] = pre_close
    df = df.rename(columns={'成交时间' : 'time', '成交价格' : 'price', '价格变动' : 'change', '成交量(手)' : 'volume', '成交额(元)' : 'amount', '性质' : 'type'})
    df['code'] = code
    df['name'] = code
    df['date'] = date
    init_price = float(df.iloc[0]['price'])
    df['open'] = init_price
    df['high'] = init_price
    df['low'] = init_price
    df['a1_p'] = init_price
    df['b1_p'] = init_price
    high = init_price
    low = init_price
    amount = 0.0
    for index, row in df.iterrows():
        if row['time'] <= '09:30:00':
           continue 
        if row['price'] > high:
           high = row['price']
        df.loc[index,'high'] = high
        if row['price'] < low:
           low = row['price']
        df.loc[index,'low'] = low
        amount += row['amount']
        df.loc[index,'amount'] = amount
        if index == 0:
           continue 
        if row['type'] == '买盘':
           df.loc[index - 1,'a1_p'] = row['price']
           df.loc[index - 1,'b1_p'] = row['price'] - 0.01
        elif row['type'] == '卖盘':
             df.loc[index - 1,'b1_p'] = row['price']
             df.loc[index - 1,'a1_p'] = row['price'] + 0.01
        else:
             df.loc[index - 1,'a1_p'] = row['price'] + 0.01     
             df.loc[index - 1,'b1_p'] = row['price'] - 0.01
    if save:         
       df.to_sql('live_' + code, con=engine, if_exists='replace') 
    return df           



def removeall(dir):
    path = os.path.join(os.path.dirname(__file__), dir) 
    for file in os.listdir(path):
        try:
           os.remove(path + '/' + file)
        except Exception as e:
               pass 

@Utils.printperformance
def loaddata(dir, save=True):
    df_list = []
    path = os.path.join(os.path.dirname(__file__), dir)
    for file in os.listdir(path):
        try:
            df = pd.read_csv(path + '/' + file, encoding='gbk', sep='\t')
            g = re.match('(sz|sh)(\d{6})(.+)(\d{8}).xls', file)
            code = g.group(2)
            pre_close = float(g.group(3))
            date = g.group(4)
            date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
            df = re_build_data(df, code, date, pre_close, save)
            df_list.append(df)
        except Exception as e:
               print('failed to load %s' % file)    
    return df_list    

# loaddata()        



