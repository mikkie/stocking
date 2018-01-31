from apscheduler.schedulers.blocking import BlockingScheduler
import time
from multiprocessing import Pool, Queue
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=3)  
def timed_job():
    print('get data ...' + time.strftime('%H:%M:%S',time.localtime(time.time())))

def calc():
    pass    

def run_job():
    sched.start()

if __name__ == '__main__':
   pool = Pool(1) 
   pool.apply_async(run_job)
   while True:
         calc()
   pool.close()
   pool.join()     


