# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-05-18'
res = []
failedRes = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','low','pre_close'], skip_paused=True, fq='pre', count=2)
        if len(df_stock) < 2:
           continue    
        first = df_stock.iloc[0]
        if first['close'] == first['open'] == first['low'] == first['high']:
           continue   
        last = df_stock.iloc[1]
        index = index.replace('.XSHE','').replace('.XSHG','') 
        if (first['close'] - first['pre_close']) / first['pre_close'] * 100 >= 9.90 and (last['open'] - last['pre_close']) / last['pre_close'] * 100 >= 3.0:
               res.append(index)
        else:
            failedRes.append(index)   
    except Exception as e:
           print(e)
        

total = len(res) + len(failedRes)        
print('win=' + str(len(res) / total * 100))  
print('loss=' + str(len(failedRes) / total * 100))            