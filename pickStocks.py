# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts

code = '600153'
year = 2017 
quarter = 2
factors = ['B/M','EPS','PEG','ROE','ROA','GP/R','P/R','L/A','FAP','CMV']


# df_k = ts.get_k_data(code)
df_hist = ts.get_hist_data(code)
df_ticket = ts.get_today_ticks(code)
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
print(df_hist)
print(df_ticket)
# print(df_basic.loc['000905']);
# print(df_report[df_report.code=='000905'].iloc[0]);
# print(df_profit[df_profit.code=='000905'].iloc[0]);
# print(df_operation[df_operation.code=='000905'].iloc[0]);
# print(df_growth[df_growth.code=='000905'].iloc[0])
# print(df_debtpaying[df_debtpaying.code=='000905'].iloc[0])
# print(df_cashflow[df_cashflow.code=='000905'].iloc[0])