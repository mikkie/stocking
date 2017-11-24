# -*-coding=utf-8-*-

__author__ = 'aqua'

import sys
import pandas as pd
import numpy as np
import tushare as ts
import datetime as dt
from utils.Utils import Utils 
from ..StrategyManager import StrategyManager


def filter(df_todayAll,setting):
    result = [];
    now = dt.datetime.now()
    todayStr = now.strftime('%Y-%m-%d')
    timeDelta = dt.timedelta(setting.get_longPeriod())
    threeMbefore = (now - timeDelta).strftime('%Y-%m-%d')
    for index,row in df_todayAll.iterrows():
        code = row['code']
        df_3m = ts.get_k_data(code,start=threeMbefore)
        df_h = ts.get_hist_data(code)
        if df_3m is None:
           continue 
        # 数据少于360天
        if df_3m.empty or len(df_3m) < setting.get_trendPeriod():
           continue 
        #添加最后一行
        if df_3m.iloc[-1].get('date') != todayStr:
           today_df = pd.DataFrame([[todayStr, row['open'],row['trade'],row['high'],row['low'],row['volume']/100,code]],columns=list(['date','open','close','high','low','volume','code']))
           df_3m = df_3m.append(today_df,ignore_index=True)
        # df_3m = df_3m[::-1]
        #计算指标使用半年D数据
        Utils.macd(df_3m)
        Utils.myKdj(df_3m)
        ######################################开始配置计算###########################################
        sm = StrategyManager()
        data = {'df_3m' : df_3m,'df_realTime' : row, 'df_h' : df_h}
        if sm.start(code, setting.get_Strategy(), data, setting):
           result.append(code) 
    return result 


def isIndicatorMatch(df_3m):
    return isKdjKingCross(df_3m)  



def isKdjKingCross(df_3m):
    yesterdayK = df_3m.iloc[-1].get('k')
    yesterdayD = df_3m.iloc[-1].get('d')
    yesterdayJ = df_3m.iloc[-1].get('j')
    lastK = df_3m.iloc[-2].get('k')
    lastD = df_3m.iloc[-2].get('d')
    lastJ = df_3m.iloc[-2].get('j')
    tdbfyK = df_3m.iloc[-3].get('k')
    tdbfyD = df_3m.iloc[-3].get('d')
    tdbfyJ = df_3m.iloc[-3].get('j')
    return lastK < 20 and lastD < 20 and lastJ < 20 and tdbfyD > tdbfyK and lastD <= lastK and yesterdayD <= yesterdayK

def isMACDkingCross(df_3m):
    yesterday = df_3m.iloc[-2].get('macd')
    lastday = df_3m.iloc[-3].get('macd')
    now = df_3m.iloc[-1].get('macd')
    if np.isnan(yesterday) or np.isnan(now) or np.isnan(lastday):
       return False 
    return (yesterday < 0 and lastday < 0 and yesterday > lastday) and (now > 0 or round(float(now), 2) == 0.00) 


def hasBigVolume(code,date):
    df_bigVolume = ts.get_sina_dd(code, date=date, vol=400)
    return True


def filterFor5Days(df_3m):
    df_3d = df_3m[-3:]
    for index,row in df_3d.iterrows():
        close = row['close']
        ma5 = row['ma5']
        if close < ma5:
           return False 
    return True
