# 启动的
import jqdata
import numpy as np
import talib as ta
import datetime


startDate = '2018-06-28'
hitDate='2018-06-27'
beforeDate = '2018-06-26'
winStop = 2.0
lossStop = -2.0
res = []
failedRes = []
ten_ten_res = []
ten_ten_failedRes = []
failed_ten_res = []
failed_ten_failedRes = []
low_list = []

ten_ten_df = []
failed_ten_df = []
ten_failed_df = []
failed_failed_df = []
today = datetime.datetime.strptime(hitDate,'%Y-%m-%d').date()

df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        df_stock = get_price(index, end_date=startDate, frequency='daily', fields=['open','close','high','high_limit','low','pre_close'], skip_paused=True, fq='pre', count=3)
        stock = get_security_info(index)
        if (today - stock.start_date).days < 30: 
            continue 
        zero = df_stock.iloc[-3] 
        if zero.name.to_pydatetime() != datetime.datetime.strptime(beforeDate,'%Y-%m-%d'):
           continue    
        first = df_stock.iloc[-2]
        if first.name.to_pydatetime() != datetime.datetime.strptime(hitDate,'%Y-%m-%d'):
           continue
        last = df_stock.iloc[-1]
        if last.name.to_pydatetime() != datetime.datetime.strptime(startDate,'%Y-%m-%d'):
           continue
        index = index.replace('.XSHE','').replace('.XSHG','') 
        if first['high'] == first['high_limit']:
           if first['close'] == first['high_limit']:
              if zero['close'] == zero['high_limit']: 
                 ten_ten_df.append(index)
              else:
                   failed_ten_df.append(index)
           else:
                if zero['close'] == zero['high_limit']: 
                   ten_failed_df.append(index)
                else:
                    failed_failed_df.append(index)   
        if (first['close'] == first['high_limit']):
            if (last['high'] - last['pre_close']) / last['pre_close'] * 100 >= winStop:
               low_p = (last['low'] - last['pre_close']) / last['pre_close'] * 100  
               if low_p < lossStop:
                  low_list.append(index) 
               res.append(index)
               if zero['close'] == zero['high_limit']:
                  ten_ten_res.append(index)
               else:
                   failed_ten_res.append(index)    
            else:
                failedRes.append(index) 
                if zero['close'] == zero['high_limit']:
                   ten_ten_failedRes.append(index)
                else:
                    failed_ten_failedRes.append(index)   
    except Exception as e:
           print(e)
        

print(u'%s号打板,%s号卖出' % (hitDate,startDate))
if len(ten_ten_df) + len(ten_failed_df) != 0:
   ratio = float(len(ten_ten_df)) / float(len(ten_ten_df) + len(ten_failed_df))
   total = len(ten_ten_res) + len(ten_ten_failedRes) 
   if total != 0:
      print(u'第二板最高涨幅>%.2f%%的概率= %.2f%%' % (winStop,ratio * float(len(ten_ten_res)) / float(total) * 100))
      print(u'第二板封板成功%.2f%% %s' % (ratio * 100,ten_ten_df))
      print(u'第二板封板失败 %s' % ten_failed_df)
      print(u'第二板最高涨幅超%.2f%% %.2f%% %s' % (winStop,float(len(ten_ten_res)) / float(total) * 100,ten_ten_res))
      print(u'第二板最高涨幅低于%.2f%% %s' % (winStop,ten_ten_failedRes))
if len(failed_ten_df) + len(failed_failed_df) != 0:
   ratio = float(len(failed_ten_df)) / float(len(failed_ten_df) + len(failed_failed_df))
   total = len(failed_ten_res) + len(failed_ten_failedRes) 
   if total != 0:
      print(u'第一板最高涨幅>%.2f%%的概率= %.2f%%' % (winStop,ratio * float(len(failed_ten_res)) / float(total) * 100))
      print(u'第一板封板成功%.2f%% %s' % (ratio * 100,failed_ten_df))
      print(u'第一板封板失败 %s' % failed_failed_df)
      print(u'第一板最高涨幅超%.2f%% %.2f%% %s' % (winStop,float(len(failed_ten_res)) / float(total) * 100,failed_ten_res))
      print(u'第一板最高涨幅低于%.2f%% %s' % (winStop,failed_ten_failedRes))
if len(ten_ten_df) + len(failed_ten_df) + len(ten_failed_df) + len(failed_failed_df) != 0:   
   ratio = float(len(ten_ten_df) + len(failed_ten_df)) / float(len(ten_ten_df) + len(failed_ten_df) + len(ten_failed_df) + len(failed_failed_df))
   total = len(res) + len(failedRes) 
   if total != 0:
      print(u'最高涨幅>%.2f%%的概率= %.2f%%' % (winStop,ratio * float(len(res)) / float(total) * 100))
# print(u'最高涨幅<%.2f%%的概率= %.2f%%' % (winStop,float(len(failedRes)) / float(total) * 100))
# print(failedRes)
# print(u'最高涨幅>%.2f%%时,最低跌幅超过%.2f%%的概率=%.2f%%' % (winStop,lossStop,float(len(low_list)) / float(len(res)) * 100))