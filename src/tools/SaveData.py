from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Pool, Queue
import os
import tushare as ts
import sys
sys.path.append('..')
from t1.datas.DataHolder import DataHolder

codeList = ['300058','603009','002911','603080','603499','601313']
sched = BlockingScheduler()
dh = DataHolder(codeList,True)

@sched.scheduled_job('interval', seconds=3)  
def timed_job():
    df = ts.get_realtime_quotes(codeList)
    dh.addData(df)

def run_job():
    sched.start()

if __name__ == '__main__':
   run_job()


