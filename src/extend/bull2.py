# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-07-13'
failed = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','high_limit','low'], skip_paused=True, fq='pre', count=90)
        flagA = False
        flag = False
        count = 0
        for index_s,row_s in df_stock.iterrows():
            if row_s['close'] == row_s['high_limit']:
               if flagA:
                  flag = True 
                  break
               else:
                   flagA = True
            else:
                flagA = False         
        if not flag:     
           failed.append(index.replace('.XSHE','').replace('.XSHG',''))
    except Exception as e:
           print(e)
        
print(failed)        