# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts

df = ts.get_k_data('002235',start='2017-01-01')
count = {'bull_bear' : 0, 'bull_bull' : 0, 'bear_bull' : 0, 'bear_bear' : 0}
percent = {'0' : 0, '0_1' : 0, '1_2' : 0, '2_3' : 0, '3_7' : 0, '7_10' : 0}
before = None
lastBefore = None
for index,row in df.iterrows():
    if lastBefore is not None:
       bv = before['close'] - before['open']
       av = row['close'] - row['open']      
       if bv > 0 and av > 0:
          count['bull_bull'] = count['bull_bull'] + 1
          p = (before['close'] - lastBefore['close']) / lastBefore['close'] * 100
          if p >= 0 and p <= 1:
             percent['0_1'] = percent['0_1'] + 1
          elif p > 1 and p <= 2:
               percent['1_2'] = percent['1_2'] + 1
          elif p > 2 and p <= 3:
               percent['2_3'] = percent['2_3'] + 1       
          elif p > 3 and p <= 7:
               percent['3_7'] = percent['3_7'] + 1
          elif p > 7:
               percent['7_10'] = percent['7_10'] + 1     
          elif p < 0:
               percent['0'] = percent['0'] + 1     
       elif bv < 0 and av < 0:
            count['bear_bear'] = count['bear_bear'] + 1
       elif bv > 0 and av < 0:
            count['bull_bear'] = count['bull_bear'] + 1
       elif bv < 0 and av > 0:
            count['bear_bull'] = count['bear_bull'] + 1 
    lastBefore = before                    
    before = row  
print('bull_bear=',count['bull_bear'])
print('bear_bear=',count['bear_bear'])
print('bear_bull=',count['bear_bull'])
print('bull_bull=',count['bull_bull'])
print('0_1=',percent['0_1'])
print('1_2=',percent['1_2'])
print('2_3=',percent['2_3'])
print('3_7=',percent['3_7'])
print('7_10=',percent['7_10'])
print('0=',percent['0'])
    
