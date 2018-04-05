# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import config.Config as conf
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR

setting = conf.Config()
engine = create_engine(setting.get_DBurl())
df_basic = ts.get_stock_basics()
df_basic.to_sql('basics',con=engine,if_exists='replace',dtype={'code': VARCHAR(df_basic.index.get_level_values('code').str.len().max())})
print('沪深上市公司基本情况数据初始化完成');


