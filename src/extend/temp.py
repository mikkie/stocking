# 启动的
import jqdata
import numpy as np
import talib as ta
import datetime


startDate = '2018-06-22'
today = datetime.datetime.strptime(startDate,'%Y-%m-%d').date()
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','high_limit','low','pre_close'], skip_paused=True, fq='pre', count=2)
        stock = get_security_info(index)
        if (today - stock.start_date).days < 30: 
            continue 
        first = df_stock.iloc[-2]
        last = df_stock.iloc[-1]
        if last['close'] == last['high_limit']:
           print((first['close'] - first['pre_close']) / first['pre_close'] * 100) 
    except Exception as e:
           print(e)
        