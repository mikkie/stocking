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
from t1.analyze.Concept import Concept
from t1.analyze.NetMoney import NetMoney
from t1.MyLog import MyLog
from utils.Utils import Utils
from sqlalchemy import create_engine
import multiprocessing as mp
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

setting = Config()
engine = create_engine(setting.get_DBurl())
thshy = pd.read_sql_table('thshy', con=engine)
thsgn = pd.read_sql_table('concept', con=engine)
analyze = Analyze(thshy,thsgn)
concept = Concept()
netMoney = NetMoney()

def run(queue):
        print('child process %s is running' % os.getpid())
        try:
            dh = None
            data = queue.get(True)
            while data is not None and data['df'] is not None and len(data['df']) > 0:
                  zs = data['zs']
                  df = data['df']
                  hygn = data['hygn']
                  netMoney = data['netMoney']
                  s = int(round(time.time() * 1000))
                  if dh is None:
                     codeList = df['code'].tolist()
                     dh = DataHolder(codeList) 
                  dh.addData(df)
                  res = analyze.calcMain(zs,dh,hygn,netMoney)
                  if len(res) > 0:
                     for code in res: 
                         dh.add_buyed(code,True)
                  MyLog.debug('process %s, calc data time = %d' % (os.getpid(),(int(round(time.time() * 1000)) - s))) 
                  data = queue.get(True)   
        except Exception as e:
               MyLog.error('error %s' % str(e))



if __name__ == '__main__':
   print('main process %s.' % os.getpid()) 

   def init(forceUpdate):
       def cb(**kw):
           return ts.get_today_all()
       df_todayAll = Utils.queryData('today_all','code',engine, cb, forceUpdate=forceUpdate)
    #    df_todayAll = df_todayAll[df_todayAll.apply(analyze.isOpenMatch2, axis=1)]
    #    return df_todayAll['code'].tolist()
       strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       while strTime < '09:30:01':
             time.sleep(0.1)
             strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
       step = setting.get_t1()['split_size']
       start = 0
       codeList = []
       length = len(df_todayAll)
       while start < length:
             end = start + step
             if end >= length:
                end = length 
             df_temp = df_todayAll.iloc[start:end]
             df = ts.get_realtime_quotes(df_temp['code'].tolist())
             df = df[df.apply(analyze.isOpenMatch, axis=1)]
             for code in df['code'].tolist():
                 codeList.append(code)
             start = end
       return codeList

   pool = mp.Pool(setting.get_t1()['process_num'])
   manager = mp.Manager()

#    codeLists = init(False)
   codeLists = ['601601','000333','000681','300188','603881','600690','300251','300271','300047','300349','600332','600229','600476','600410','600315','300244','002236','002024','300212','300253','603888','600728','002396','600446','002415','002488','601116','600797','600037','600662','002697','000902','601777','002609','601866','000882','600398','002223','601216','600028','000516','600130','300027','000156','002739','601929','300339','300279','600640','600026','002505','000698','000831','600280','002421','600757','300274','002264','600723','000670','600604','000058','600936','600104','600827','002157','002170','002065','000607','002139','600289','002543','601928','002401','300245','600588','600718','600055','000639','300161','600633','300020','000756','002094','603001','002153','000665','002368','002530','603258','300638','600258','000503','000020', '000023', '000025', '000037', '000410', '000503', '000530', '000665', '000670', '000693', '000738', '000790', '000882', '000948', '002076', '002137', '002141', '002184', '002226', '002232', '002281', '002370', '002402', '002454', '002497', '002532', '002606', '002629', '002645', '002676', '002694', '002698', '002702', '002769', '002795', '002847', '002848', '002861', '002863', '002877', '002883', '002903', '002907', '002911', '002913', '002916', '002927', '002928', '002929', '300066', '300073', '300085', '300099', '300104', '300216', '300236', '300237', '300269', '300300', '300302', '300344', '300353', '300378', '300420', '300462', '300477', '300479', '300487', '300490', '300520', '300556', '300560', '300586', '300609', '300612', '300644', '300647', '300649', '300650', '300672', '300675', '300678', '300684', '300688', '300698', '300707', '300715', '300730', '300731', '300738', '300740', '600136', '600139', '600198', '600207', '600213', '600405', '600433', '600490', '600577', '600579', '600588', '600610', '600652', '600721', '600728', '600804', '600868', '600901', '600903', '600962', '601366', '603006', '603056', '603058', '603059', '603083', '603329', '603506', '603516', '603533', '603559', '603616', '603778', '603895', '603986', '603988']
   print('calc stocks %s' % codeLists)
   codeSplitMaps = {} 
   queueMaps = {}
   interDataHolder = {
      'currentTime' : dt.datetime.now(),
      'hygn' : concept.getCurrentTopHYandConcept(),
      'netMoney' : netMoney.getNetMoneyRatio()
   }

   for code in setting.get_ignore():
       if code in codeLists:
          codeLists.remove(code)  
   length = len(codeLists)
   print('calc stocks size %d' % length) 
   step = setting.get_t1()['split_size']
   x = length // setting.get_t1()['process_num']
   y = length % setting.get_t1()['process_num']
   if x + y < setting.get_t1()['split_size']:
      step = x + y
   begin = 0
   less = 1
   if length % step == 0: 
      less = 0
   num_splits = length // step + less
   for i in range(num_splits):
       end = begin + step
       if end > length:
          end = length 
       code_split = codeLists[begin:end]
       codeSplitMaps[i] = code_split
       queue = manager.Queue()
       queueMaps[i] = queue
       pool.apply_async(run, (queue,))
       begin = end
       if begin >= length:
          break

   sched = BlockingScheduler()

   @sched.scheduled_job('interval', seconds=setting.get_t1()['get_data_inter'])
   def getData():
       now = dt.datetime.now()
       if (now - interDataHolder['currentTime']).seconds > 30:
          interDataHolder['currentTime'] = now
          hygn = concept.getCurrentTopHYandConcept()
          if hygn is not None:
             interDataHolder['hygn'] = hygn 
          net = netMoney.getNetMoneyRatio()
          if netMoney is not None:
             interDataHolder['netMoney'] = net
       for key in codeSplitMaps:
           df = ts.get_realtime_quotes(codeSplitMaps[key])
           zs = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
           queueMaps[key].put({'zs' : zs,'df' : df,'hygn' : interDataHolder['hygn'],'netMoney' : interDataHolder['netMoney']})
        #    for debug     
        #    d = df[df['code'] == '300063']
        #    if d is not None and len(d) > 0:
        #       print('key=' + str(key))
        #       print('300063')

   sched.start()

   pool.close()
   pool.join()