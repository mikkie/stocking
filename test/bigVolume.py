# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
from sqlalchemy import create_engine

df = ts.get_sina_dd('000885', date='2017-12-05',vol=400)
df['total'] = df['price'] * df['volume']
buy = df.loc[df['type'] == '买盘', 'total'].sum()
sell = df.loc[df['type'] == '卖盘', 'total'].sum()
print(df)
print(buy)
print(sell)
# df_ticket = ts.get_tick_data('000856',date='2017-11-09')
# engine = create_engine('mysql://root:aqua@127.0.0.1/stocking?charset=utf8')
# df_ticket.to_sql('today_tickets',engine,if_exists='replace')
# print(df_ticket)