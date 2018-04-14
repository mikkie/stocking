# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-04-13'
res = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','low'], skip_paused=True, fq='pre', count=60)
        if len(df_stock) < 15:
           continue    
        countContinue10 = 0    
        pre_close = None
        flag = False
        for index_s,row_s in df_stock.iterrows():
            if pre_close is None:
               pre_close = row_s['close']
               continue
            if (row_s['close'] - pre_close) / pre_close * 100 >= 9.93:
               countContinue10 = countContinue10 + 1
               if countContinue10 >= 2:
                  flag = True
                  break 
            else:
                countContinue10 = 0    
            pre_close = row_s['close']
        # if count_close < 8 or count_ma5 < 8:
        #    flag = False
        # if count_10 < 1 or count_10 > 4:
        #    flag = False
        # if (lastClose - low) / (high - low) > 0.8:
        #    flag = False   
        # if flag == False:
        #    continue    
        # df_stock = df_stock[-4:]
        # pre_close = None
        # for index_s,row_s in df_stock.iterrows():
        #     if pre_close is None:
        #        pre_close = row_s['close']
        #        continue
        #     if (row_s['close'] - pre_close) / pre_close * 100 >= 7:
        #        flag = False
        #        break
        #     pre_close = row_s['close']
        if flag:
           index = index.replace('.XSHE','').replace('.XSHG','') 
           res.append(index)
    except Exception as e:
           print(e)
        
print(res)            