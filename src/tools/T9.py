# -*-coding=utf-8-*-
__author__ = 'aqua'
#Mock数据
import tushare as ts
import threading
import time
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append('..')
from config.Config import Config 
from t1.MyLog import MyLog
from t1.datas.DataHolder import DataHolder
from t1.analyze.Analyze import Analyze
from t1.analyze.Concept import Concept
from t1.analyze.NetMoney import NetMoney
from t1.trade.MockTrade import MockTrade

codes = ['002507','002903','300404','603969']
src_datas = {}
datas = {}
setting = Config()
engine = create_engine(setting.get_DBurl())
dh = DataHolder(codes)
# thshy = pd.read_sql_table('thshy', con=engine)
# thsgn = pd.read_sql_table('concept', con=engine)
# analyze = Analyze(thshy,thsgn)
analyze = Analyze(None,None)
mockTrade = MockTrade()
mockTrade.relogin()
# concept = Concept()
# netMoney = NetMoney()
# hygn = concept.getCurrentTopHYandConcept()
# net = netMoney.getNetMoneyRatio()
zs = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])

for code in codes:
    try:
       src_datas[code] = pd.read_sql_table('live_' + code, con=engine)
    except Exception as e:
           MyLog.error('read mock data error \n')
           MyLog.error(str(e) +  '\n')   

def run(i):
    df = pd.DataFrame()
    for code in src_datas:
        if i < len(src_datas[code]):
           df = df.append(src_datas[code].iloc[i])
    if len(df) > 0:
       dh.addData(df)
       codes = analyze.calcMain(zs,dh,None,None)
       if len(codes) > 0:
          for code in codes: 
              dh.add_buyed(code,False)

for i in range(5200):
    run(i)
