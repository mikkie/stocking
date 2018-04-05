from apscheduler.schedulers.blocking import BlockingScheduler
import time
from multiprocessing import Pool, Queue
import os
import tushare as ts

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=3)  
def timed_job():
    # print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    df = ts.get_realtime_quotes(['002460'])
    print(df.iloc[0]['time'])

def run_job():
    sched.start()

if __name__ == '__main__':
   run_job()


