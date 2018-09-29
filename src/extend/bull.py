# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-09-28'
res = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','low','avg'], skip_paused=True, fq='pre', count=5)
        if len(df_stock) < 5:
           continue        
        avg = df_stock['avg'].mean()
        lastClose = df_stock.iloc[-1].get('close')
        if (lastClose - avg) / avg > 0.05:
           index = index.replace('.XSHE','').replace('.XSHG','') 
           res.append(index)
    except Exception as e:
           print(index)
        
print(res)            