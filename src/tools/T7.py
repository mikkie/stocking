# -*-coding=utf-8-*-
__author__ = 'aqua'
#从tushare实时获取数据
import tushare as ts
import threading
import time
import pandas as pd
import sys
sys.path.append('..')
from config.Config import Config
from t1.datas.DataHolder import DataHolder
from t1.analyze.Analyze import Analyze
from utils.Utils import Utils
from sqlalchemy import create_engine

# codes = ['002839', '300417', '300344', '000885', '002863', '300107', '000737', '000702', '002762', '600133', '002125', '300631', '603050', '600325', '600093', '000036', '600684', '603031', '300487', '600939', '002771', '300113', '000011', '002861', '002494', '000055', '002279', '603926', '300542', '300058', '300348', '603823', '002235', '002865', '002846', '002233', '600470', '000608', '002748', '600202', '601228', '603787', '300288', '600802', '600624', '300184', '603817', '603058', '600892', '600908', '300044', '002807', '601212', '600606', '300162', '300573', '601128', '002040', '603009', '600381', '000877', '000732', '300418', '601881', '300287', '300531', '300052', '300481', '300379', '603323', '002797', '603319', '300428', '300047', '600623', '002657', '002810', '603101', '300407', '603320', '002802', '300588', '603958', '600727', '002862', '000881', '002847', '002836', '601595', '603969', '300528', '002063', '600506', '603826', '002766', '300647', '300537', '601858', '000962', '002743', '000603', '603159', '002719', '300539', '300592', '300368', '300611', '300491', '300632', '002774', '002457', '603036', '300556', '300137', '002848', '603717', '002826', '603727', '002767', '300534', '000014', '300465', '300191', '300541', '600072', '000912', '300380', '000856', '600855']
setting = Config()
engine = create_engine(setting.get_DBurl())
analyze = Analyze()

def get_today_all_codes():
    def cb(**kw):
        return ts.get_today_all()
    df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=False)
    return df_todayAll['code']

def run(codes,dh):
    df = ts.get_realtime_quotes(codes)
    dh.addData(df)
    res = analyze.calcMain(dh)
    if res != '':
       dh.add_buyed(res) 
    global timer
    timer = threading.Timer(setting.get_t1()['get_data_inter'], run, args=[codes,dh])
    timer.start()

threads = []
codes = get_today_all_codes()
length = len(codes)
begin = 0
num_threads = length // 100 + 1
for i in range(num_threads):
    end = begin + 100
    if end > length:
       end = length 
    df_codes = codes[begin:end]
    code_list = df_codes.tolist()
    dh = DataHolder(code_list)
    t = threading.Thread(target=run, args=(code_list,dh))   
    t.setDaemon(True)
    t.start()
    threads.append(t)
    begin = end
    if begin >= length:
       break
    for t in threads:
        t.join()  

while True:
      time.sleep(1)
pass