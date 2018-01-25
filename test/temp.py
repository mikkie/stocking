# -*-coding=utf-8-*-
__author__ = 'aqua'


import tushare as ts
from sqlalchemy.types import VARCHAR
from sqlalchemy import create_engine

print(ts.get_realtime_quotes(['002839']))

# engine = create_engine('mysql://root:aqua@127.0.0.1/stocking?charset=utf8')

# df = ts.get_stock_basics() 
# # print(df)
# df.to_sql('basics',engine,if_exists='replace',index_label='code',dtype={'code': VARCHAR(df.index.get_level_values('code').str.len().max())})   


# df = ts.get_profit_data(2017,3)
# # print(df)
# df.to_sql('profit',engine,if_exists='replace',index_label='code',index=False)

# df = ts.get_growth_data(2017,3)
# # print(df)
# df.to_sql('growth',engine,if_exists='replace',index_label='code',index=False)