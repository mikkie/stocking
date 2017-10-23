# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import talib as ta
import pandas as pd
from sqlalchemy import create_engine

code = '600153'

df_ticket = ts.get_today_ticks(code)
df_ticket = df_ticket.iloc[::-1]
print(df_ticket)
engine = create_engine('mysql://root:aqua@127.0.0.1/stocking?charset=utf8')
df_ticket.to_sql('tickets',engine,if_exists='append')