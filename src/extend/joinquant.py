# 还未启动的
import jqdata
import numpy as np
import talib as ta

res = []
df_all = get_all_securities(types=['stock'], date='2018-03-22')
for index,row in df_all.iterrows():
    df_stock = get_price(index, end_date='2018-03-22', frequency='daily', fields=['close','high','low'], skip_paused=True, fq='pre', count=90)
    high_row = df_stock.loc[df_stock['high'].idxmax()]
    high = high_row.get('high')
    low_row = df_stock.loc[df_stock['low'].idxmin()]
    low = low_row.get('low')
    lastClose = df_stock.iloc[-1].get('close')
    close = df_stock['close'].values
    df_stock['ma5'] = ta.SMA(close,timeperiod=5)
    df_stock['ma10'] = ta.SMA(close,timeperiod=10)
    df_stock = df_stock[-15:]
    pre_close = None
    flag = True
    count_close = 0
    count_ma5 = 0
    for index_s,row_s in df_stock.iterrows():
        if pre_close is None:
           pre_close = row_s['close']
           continue
        if (row_s['close'] - pre_close) / pre_close * 100 > 5 or (row_s['close'] - pre_close) / pre_close * 100 < -5:
           flag = False 
           break
        ma5 = row_s['ma5']
        ma10 = row_s['ma10']
        if not np.isnan(ma5) and not np.isnan(ma10):
           if row_s['close'] > ma5:
              count_close = count_close + 1
           if ma5 > ma10:
              count_ma5 = count_ma5 + 1      
        pre_close = row_s['close']
    if count_close < 10 or count_ma5 < 10:
       flag = False 
    if (lastClose - low) / (high - low) > 0.4:
       flag = False 
    if flag:
       index = index.replace('.XSHE','').replace('.XSHG','') 
       res.append(index)
print(res)