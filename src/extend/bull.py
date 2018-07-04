# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-07-04'
res = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','low'], skip_paused=True, fq='pre', count=120)
        if len(df_stock) < 60:
           continue        
        high_row = df_stock.loc[df_stock['high'].idxmax()]
        high = high_row.get('high')
        low_row = df_stock.loc[df_stock['low'].idxmin()]
        low = low_row.get('low')
        lastClose = df_stock.iloc[-1].get('close')
        if (lastClose - low) / (high - low) > 0.8:
           index = index.replace('.XSHE','').replace('.XSHG','') 
           res.append(index)
    except Exception as e:
           print(index)
        
print(res)            