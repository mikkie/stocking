# 启动的
import jqdata
import numpy as np
import talib as ta


startDate = '2018-05-31'
res = []
failedRes = []
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','high_limit'], skip_paused=True, fq='pre', count=1)
        first = df_stock.iloc[0]
        if first['high'] == first['high_limit']:
           if first['close'] == first['high_limit']:    
              res.append(index)
           else:
                failedRes.append(index)   
    except Exception as e:
           print(e)
        

total = len(res) + len(failedRes) 
print(u'封板成功的概率= %.2f%%' % (float(len(res)) / float(total) * 100))
print(res)
print(u'封板失败的概率= %.2f%%' % (float(len(failedRes)) / float(total) * 100))
print(failedRes)