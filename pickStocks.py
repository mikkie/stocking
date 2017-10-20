# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import talib as ta
import pandas as pd

code = '600153'
# year = 2017 
# quarter = 2
# factors = ['B/M','EPS','PEG','ROE','ROA','GP/R','P/R','L/A','FAP','CMV']


def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    ewma12 = pd.ewma(price,span=fastperiod)
    ewma60 = pd.ewma(price,span=slowperiod)
    dif = ewma12-ewma60
    dea = pd.ewma(dif,span=signalperiod)
    bar = 2 * (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar


# df_k = ts.get_k_data(code)
df_hist = ts.get_hist_data(code,ktype='5')
df_hist = df_hist.iloc[::-1]
close = df_hist.close.values  #ndarray
df_hist['dif'], df_hist['dea'], df_hist['macd'] = myMACD(close, fastperiod=12, slowperiod=26, signalperiod=9) #series
# df_hist['macd'] = df_hist['macd'] * 2;

# df_ticket = ts.get_today_ticks(code)
# df_basic = ts.get_stock_basics()
# df_report = ts.get_report_data(year,quarter)
# df_profit = ts.get_profit_data(year,quarter)
# df_operation = ts.get_operation_data(year,quarter)
# df_growth = ts.get_growth_data(year,quarter)
# df_debtpaying = ts.get_debtpaying_data(year,quarter)
# df_cashflow = ts.get_cashflow_data(year,quarter)

# df_basic['B/M'] = 1/df_basic['pb']
# pe = df_basic.loc['000905','pe']
# epsg = abs(df_growth[df_growth.code=='000905'].iloc[0].get('epsg'))

# print(df_k)
print(df_hist.tail(48))
# print(df_ticket)
# print(df_basic.loc['000905']);
# print(df_report[df_report.code=='000905'].iloc[0]);
# print(df_profit[df_profit.code=='000905'].iloc[0]);
# print(df_operation[df_operation.code=='000905'].iloc[0]);
# print(df_growth[df_growth.code=='000905'].iloc[0])
# print(df_debtpaying[df_debtpaying.code=='000905'].iloc[0])
# print(df_cashflow[df_cashflow.code=='000905'].iloc[0])