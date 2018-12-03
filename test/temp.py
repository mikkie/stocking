# -*-coding=utf-8-*-
__author__ = 'aqua'

import time
import pandas as pd
import tushare as ts
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    
   def init():
       df = pd.DataFrame([{'aa' : 1, 'bb' : 2},{'aa' : 1, 'bb' : 2},{'aa' : 1, 'bb' : 2}])
       return (df['aa'].tolist(),df['bb'].tolist(),4) 
   
   aa,bb,cc = init()

   sched = BlockingScheduler()

   @sched.scheduled_job('interval', id="a", seconds=3,max_instances=10)
   def a():    
       global aa
       print(aa)
       aa = 'aa'


   @sched.scheduled_job('interval', id="b", seconds=5,max_instances=10)
   def b():    
       print(bb)   


   sched.start()

   while True:
         time.sleep(10)
