# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-08-03'
failed = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','high_limit','low'], skip_paused=True, fq='pre', count=30)
        count = 0
        flag = False
        for index_s,row_s in df_stock.iterrows():
            if row_s['close'] == row_s['high_limit']:
               if count == 3:
                  flag = True 
                  break
               else:
                   count += 1
            else:
                count = 0         
        if flag:     
           failed.append(index.replace('.XSHE','').replace('.XSHG',''))
    except Exception as e:
           print(e)
        
print(failed)        