# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import pandas as pd

count = {'-10_-8' : 0 , '-8_-6' : 0 ,'-6_-4' : 0 ,'-4_-2' : 0 ,'-2_0' : 0, '0_2' : 0, '2_4' : 0,'4_6' : 0, '6_8' : 0, '8_10' : 0}

def run(df,flag):
    percent = {'-10_-8' : 0 , '-8_-6' : 0 ,'-6_-4' : 0 ,'-4_-2' : 0 ,'-2_0' : 0, '0_2' : 0, '2_4' : 0,'4_6' : 0, '6_8' : 0, '8_10' : 0}
    yesterday = None
    theDayBeforeYesterday = None
    for index,row in df.iterrows():
       if theDayBeforeYesterday is not None:
          p = (row['close'] - yesterday['close']) / yesterday['close'] * 100
          if bool(p > 0) == bool(flag):
             p_before = (yesterday['close'] - theDayBeforeYesterday['close']) / theDayBeforeYesterday['close'] * 100 
             if p_before >= -10 and p_before < -8:
                percent['-10_-8'] = percent['-10_-8'] + 1
             elif p_before >= -8 and p_before < -6:
                  percent['-8_-6'] = percent['-8_-6'] + 1
             elif p_before >= -6 and p_before < -4:
                  percent['-6_-4'] = percent['-6_-4'] + 1
             elif p_before >= -4 and p_before < -2:
                  percent['-4_-2'] = percent['-4_-2'] + 1
             elif p_before >= -2 and p_before < 0:
                  percent['-2_0'] = percent['-2_0'] + 1   
             elif p_before >= 0 and p_before < 2:
                  percent['0_2'] = percent['0_2'] + 1
             elif p_before >= 2 and p_before < 4:
                  percent['2_4'] = percent['2_4'] + 1
             elif p_before >= 4 and p_before < 6:
                  percent['4_6'] = percent['4_6'] + 1
             elif p_before >= 6 and p_before < 8:
                  percent['6_8'] = percent['6_8'] + 1     
             elif p_before >= 8 and p_before < 10:
                  percent['8_10'] = percent['8_10'] + 1                    
       theDayBeforeYesterday = yesterday                    
       yesterday = row 
    return percent 

def start(code,count):
    df = ts.get_k_data(code,start='2017-01-01')
    rowList = []
    rowList.append(run(df,True))
    rowList.append(run(df,False))
    df = pd.DataFrame(rowList)
    # print(df)
    total = df.sum()
    a = df.iloc[0]/total * 100
    b = df.iloc[1]/total * 100
    # print('当日涨幅次日收阳的概率====\n',a) 
    # print('当日涨幅次日收阴的概率====\n',b)
    key = a.idxmax()
    count[key] = count[key] + 1

df = ts.get_today_all()
for index,row in df.iterrows():
    code = row['code']
    start(code,count)

print(count)    

   
 
    
