# -*-coding=utf-8-*-
__author__ = 'aqua'

import sys
sys.path.append('..')
from config.Config import Config
import tushare as ts
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR


setting = Config()
engine = create_engine(setting.get_DBurl())

df_basic = None
df_rd = None
basics = setting.get_Basic()

if setting.get_updateToday():
   df_basic = ts.get_stock_basics()
   df_basic.to_sql('basics',engine,if_exists='replace',index_label='code',dtype={'code': VARCHAR(df_basic.index.get_level_values('code').str.len().max())})

   df_rd = ts.get_report_data(basics[0],basics[1])
   df_rd.to_sql('report',engine,if_exists='replace',index_label='code',index=False)

df_basic = pd.read_sql_table('basics', con=engine)  
df_rd = pd.read_sql_table('report', con=engine)
    
for index,row in df_basic.iterrows():
    code = row['code']
    if row['pe'] < basics[2]:
       rd_row = df_rd.loc[df_rd['code'] == code]
       if len(rd_row) > 0:
          rd_row = rd_row.iloc[-1] 
          if rd_row['eps'] > basics[3] and rd_row['roe'] > basics[5] and rd_row['profits_yoy'] > basics[6]:
            #  and rd_row['bvps'] > basics[4] 
            #  and 
             print(code)