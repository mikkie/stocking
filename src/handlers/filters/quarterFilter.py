# -*-coding=utf-8-*-

__author__ = 'aqua'

import pandas as pd
import numpy as np
import tushare as ts
import datetime as dt
from utils.Utils import Utils 


def filterSuperSoldIn3Months(df_todayAll,setting):
    result = [];
    now = dt.datetime.now()
    timeDelta = dt.timedelta(setting.get_longPeriod())
    threeMbefore = (now - timeDelta).strftime('%Y-%m-%d')
    for index,row in df_todayAll.iterrows():
        code = row['code']
        df_3m = ts.get_hist_data(code,start=threeMbefore,ktype='D')
        # 数据少于90天
        if df_3m.empty or len(df_3m) < 30 * 3:
           continue 
        #倒序
        df_3m = df_3m[::-1]
        #计算指标使用半年D数据
        Utils.macd(df_3m)
        #计算一季度的值
        df_3m = df_3m[-90:]
        # print(df_3m)
        high = df_3m.loc[df_3m['high'].idxmax()].get('high')
        low = df_3m.loc[df_3m['low'].idxmin()].get('low')
        # p_change = df_3m['p_change'].mean()
        close = df_3m.iloc[-1].get('close')
        if np.isnan(high) or np.isnan(low) or np.isnan(close):
           continue 
        ratio = (close - low) / (high - low)
        if isMACDkingCross(df_3m) and ratio < setting.get_SuperSold()[1] and ratio > setting.get_SuperSold()[0]:
           print(code)
           result.append(code)
    return result 

def isMACDkingCross(df_3m):
    yesterday = df_3m.iloc[-2].get('macd')
    lastday = df_3m.iloc[-3].get('macd')
    now = df_3m.iloc[-1].get('macd')
    if np.isnan(yesterday) or np.isnan(now) or np.isnan(lastday):
       return False 
    return (yesterday < 0 or lastday < 0) and now > 0