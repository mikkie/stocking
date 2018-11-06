# 连续两日涨停
import jqdata
import numpy as np
import talib as ta

startDate = '2018-11-06'
res = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['close','high','low'], skip_paused=True, fq='pre', count=90)
    df_stock = df_stock[-3:]
    pre_close = None
    flag = False
    count_10 = 0
    for index_s,row_s in df_stock.iterrows():
        if pre_close is None:
           pre_close = row_s['close']
           continue
        if (row_s['close'] - pre_close) / pre_close * 100 >= 9.90:
           count_10 = count_10 + 1
        pre_close = row_s['close']
    if count_10 == 2:
       flag = True
    if flag:
       index = index.replace('.XSHE','').replace('.XSHG','') 
       res.append(index)
print(res)


