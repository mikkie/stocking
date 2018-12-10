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
from t1.analyze.SellAnalyze import SellAnalyze
from utils.Utils import Utils

codes = ['300116']
src_datas = {}
datas = {}
setting = Config()
engine = create_engine(setting.get_DBurl())
dh = DataHolder(codes)
# thshy = pd.read_sql_table('thshy', con=engine)
# thsgn = pd.read_sql_table('concept', con=engine)
# analyze = Analyze(thshy,thsgn)
analyze = SellAnalyze()
mockTrade = MockTrade()
mockTrade.relogin()
# concept = Concept()
# netMoney = NetMoney()
# hygn = concept.getCurrentTopHYandConcept()
# net = netMoney.getNetMoneyRatio()
# zs = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])

def run(i):
    df = pd.DataFrame()
    for code in src_datas:
        if i < len(src_datas[code]):
           df = df.append(src_datas[code].iloc[i])
    if len(df) > 0:
       dh.addSellData(df)
       analyze.calcMain(None,dh)


@Utils.printperformance
def start_test_by_df(df_list):
    for df in df_list:
        try:
            code = df.iloc[0]['code']
            src_datas[code] = df
        except Exception as e:
               MyLog.error('read mock data error \n')
               MyLog.error(str(e) +  '\n') 
    for i in range(5200):
        run(i)

