# -*-coding=utf-8-*-
__author__ = 'aqua'

import easytrader
import json
import datetime as dt
from ..MyLog import MyLog

class Trade(object):

      def __init__(self):
          self.__user = easytrader.use('ths')
          self.__user.connect(r'C:/xyzqdlxd/xiadan.exe')


      def buy(self,code,amout,price):
          try:
              res = self.__user.buy(code, price=price, amount=amout)
              MyLog.info(res)
              return res
          except Exception as e:
                 MyLog.info('交易失败code = %s,price = %s, amount = %s, e = %s' % (code,price,amout,e))
                 return ''


      def cancelBuy(self,code):
          j = self.__user.today_entrusts
          if len(j) > 0:
             for stock in j:
                 if stock['证券代码'] == code and stock['买卖标志'] == '买入' and (int(stock['委托数量']) - int(stock['成交数量']) - int(stock['撤单数量'])) > 0:
                    self.__user.cancel_entrust(stock['委托序号'])
                    return 0
          return -1      

      def cancelAllBuy(self):
          j = self.__user.today_entrusts
          if len(j) > 0:
             for stock in j:
                 if stock['买卖标志'] == '买入' and (int(stock['委托数量']) - int(stock['成交数量']) - int(stock['撤单数量'])) > 0:
                    self.__user.cancel_entrust(stock['委托序号'])                          


      def queryBuyStocks(self):
          j = self.__user.today_trades
          buyCount = 0
          if len(j) > 0:
             for stock in j:
                 if stock['买卖标志'] == '买入' and int(stock['成交数量']) > 0:
                    buyCount = buyCount + 1
          return buyCount            



      def sell(self,code,price):
          try:
             isSelled = True
             j = self.__user.today_entrusts
             if len(j) > 0:
                for stock in j:
                    if stock['证券代码'] == code and stock['买卖标志'] == '卖出' and (int(stock['委托数量']) - int(stock['成交数量']) - int(stock['撤单数量'])) > 0:
                        isSelled = False 
                        ct = dt.datetime.strptime(stock['委托日期'] + ' ' + stock['委托时间'], '%Y%m%d %H:%M:%S')
                        if (dt.datetime.now() - ct).seconds > 30: 
                           self.__user.cancel_entrust(stock['委托序号'])
             j = self.__user.position
             if len(j) > 0:
                for stock in j:
                    if stock['证券代码'] == code and int(stock['股份可用']) > 0:
                       isSelled = False
                       self.__user.sell(code, price=price, amount=int(stock['股份可用']))   
             return isSelled
          except Exception as e:
                 MyLog.info('sell [%s] error' % code)
                 return False  


# trade = Trade()
# trade.sell('002012',7.69)                 
          