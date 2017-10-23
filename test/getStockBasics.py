# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
from sqlalchemy import create_engine

df_basic = ts.get_stock_basics()
print(df_basic);
engine = create_engine('mysql://root:aqua@10.172.97.136/stocking?charset=utf8')
df_basic.to_sql('basics',engine,if_exists='append')
