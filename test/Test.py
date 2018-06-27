# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare
import threading
import time
import datetime

l = ['603999', '603996', '603988', '603987', '603978', '603977', '603976', '603970', '603969', '603966', '603963', '603960', '603959', '603958', '603955', '603937', '603936', '603933', '603929', '603928', '603922', '603920', '603917', '603916', '603912', '603908', '603906', '603903', '603897', '603890', '603888', '603887', '603886', '603882', '603881', '603876', '603861', '603860', '603859', '603856', '603848', '603829', '603826', '603822', '603819', '603817', '603813', '603811', '603809', '603803', '603800', '603798', '603797', '603779', '603778', '603777', '603776', '603738', '603733', '603727', '603725', '603722', '603721', '603717', '603716', '603712', '603711', '603709', '603707', '603703', '603701', '603689', '603688', '603685', '603683', '603680', '603677', '603676']
r = ['sh','sz','hs300','sz50','zxb','cyb']
# print(tushare.get_realtime_quotes(l))

def fun_timer():
    try:
       starttime = datetime.datetime.now()
       tushare.get_realtime_quotes(l)
       endtime = datetime.datetime.now()
       print((endtime - starttime).seconds)
    except Exception as e:
           print(e)
           pass   
    global timer
    timer = threading.Timer(3, fun_timer)
    timer.start()

timer = threading.Timer(3, fun_timer)
timer.start()


