# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
from sqlalchemy import create_engine

df_basic = ts.get_stock_basics()
print(df_basic);
engine = create_engine('mysql://root:aqua@127.0.0.1/stocking?charset=utf8')
df_basic.to_sql('basics',engine,if_exists='replace',index_label='code',dtype={'code': VARCHAR(df_basic.index.get_level_values('code').str.len().max())})
