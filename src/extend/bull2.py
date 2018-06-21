# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-06-21'
failed = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','high_limit','low'], skip_paused=True, fq='pre', count=180)
        flag = False
        count = 0
        for index_s,row_s in df_stock.iterrows():
            if row_s['close'] == row_s['high_limit']:
               count = count + 1
               if count >= 1:  
                  flag = True
                  break
        if not flag:     
           failed.append(index.replace('.XSHE','').replace('.XSHG',''))
    except Exception as e:
           print(e)
        
print(failed)        