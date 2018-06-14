# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-05-13'
hitDate='2018-05-12'
winStop = 3.0
lossStop = -2.0
res = []
failedRes = []
low_list = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','low','pre_close'], skip_paused=True, fq='pre', count=2)
        if len(df_stock) < 2:
           continue    
        first = df_stock.iloc[0]
        last = df_stock.iloc[1]
        if first['close'] == first['open'] and first['close'] == first['low'] and first['close'] == first['high']:
               continue   
        index = index.replace('.XSHE','').replace('.XSHG','') 
        if (first['close'] - first['pre_close']) / first['pre_close'] * 100 >= 9.90:
            if (last['high'] - last['pre_close']) / last['pre_close'] * 100 >= winStop:
               low_p = (last['low'] - last['pre_close']) / last['pre_close'] * 100  
               if low_p < lossStop:
                  low_list.append(index) 
               res.append(index)
            else:
                failedRes.append(index)   
    except Exception as e:
           print(e)
        

total = len(res) + len(failedRes) 
print(u'%s号打板,%s号卖出' % (hitDate,startDate))
print(u'最高涨幅>%.2f%%的概率= %.2f%%' % (winStop,float(len(res)) / float(total) * 100))
print(res)
print(u'最高涨幅<%.2f%%的概率= %.2f%%' % (winStop,float(len(failedRes)) / float(total) * 100))
print(failedRes)
print(u'最高涨幅>%.2f%%时,最低跌幅超过%.2f%%的概率=%.2f%%' % (winStop,lossStop,float(len(low_list)) / float(len(res)) * 100))