# -*-coding=utf-8-*-
__author__ = 'aqua'

import easytrader
import json
import os
import datetime as dt
import psutil
import time
# import sys
# sys.path.append('..')
# import MyLog
from ..MyLog import MyLog

class Trade(object):

      def __init__(self,isSell=False):
          self.__user = easytrader.use('ths')
          if isSell:
             if not self.judgeprocess('xiadan.exe'):
                os.popen(r'C:/aqua/stock/dlxd-sell/xiadan.exe') 
                time.sleep(30)   
             self.__user.connect(r'C:/aqua/stock/dlxd-sell/xiadan.exe') 
          else: 
              if not self.judgeprocess('xiadan.exe'):
                 os.popen(r'C:/aqua/stock/dlxd/xiadan.exe')   
                 time.sleep(30)     
              self.__user.connect(r'C:/aqua/stock/dlxd/xiadan.exe')


      def judgeprocess(self, processname):
          pl = psutil.pids()
          for pid in pl:
              if psutil.Process(pid).name() == processname:
                 return True
          return False    

      def buy(self,code,amout,price):
          try:
              if self.__user.buy(code, price=price, amount=amout):
                 MyLog.info('buyed %s' % code)
                 return {'message' : 'success'}
              return {'message' : 'failed'}   
          except Exception as e:
                 MyLog.info('交易失败code = %s,price = %s, amount = %s, e = %s' % (code,price,amout,e))
                 return {'message' : 'failed'}


      def refresh(self):
          try:
              self.__user._click_refresh()
          except Exception as e:
                 MyLog.info('refresh trade failed')     

      def cancel(self,code,isBuy):
          try:
             self.__user.cancel_entrust(code=code,isBuy=isBuy)
             MyLog.info('cancel code = %s isBuy = %s'  % (code,isBuy))
             return 0
          except Exception as e:
                 MyLog.info('撤单code = %s失败, e = %s' % (code,e))
                 return -1   


      def queryBuyStocks(self):
          try:
              j = self.__user.today_trades
              buyCount = 0
              if len(j) > 0:
                 for stock in j:
                     if stock['操作'].find('买入') >= 0 and int(stock['成交数量']) > 0:
                        buyCount = buyCount + 1
              return buyCount
          except Exception as e:
                 MyLog.info('查询当日买入数量失败,%s' % e)
                 return 0    


      def queryBalance(self):
          try:
              return self.__user.balance
          except Exception as e:
                 MyLog.info('查询可用金额失败,%s' % e)
                 return None                    



      def sell(self,code,price,amount=None):
          try:
             self.cancel(code,False)
             res = self.__user.sell(code, price=price, amount=amount) 
             MyLog.info('卖出code = %s' % code)
             return res
          except Exception as e:
                 MyLog.info('卖出code = %s失败, e = %s' % (code,e))
                 return False    


# trade = Trade()
# #buy1
# trade.buy('300022',100,4.68)
# #buy1
# trade.buy('002031',100,2.47)
# #buy3
# trade.buy('002481',100,4.91)
# # cancel1
# trade.cancel('300022',True)
# #cancel2
# trade.cancel('002031',True) 
# #cancel all
# trade.cancel(None,True) 
# #cancel again
# trade.cancel('002031',True) 
# #sell1
# trade.buy('002121',100,5.85)

# trade.sell('002121',5.80)

# trade.sell('002121',7.14)
# #sell2
# trade.sell('002031',3.41) 

# trade.sell('002121',7.13)

# trade.sell('002031',3.40)
# #cancel sell
# trade.cancel('002031',False) 
# #count buy
# trade.refresh()     
# print(trade.queryBuyStocks())        
# 
          