# -*-coding=utf-8-*-
__author__ = 'aqua'

import easytrader

class Trade(object):

      def __init__(self):
          self.__user = easytrader.use('ths')
          self.__user.connect(r'C:/xyzqdlxd/xiadan.exe')


      def buy(self,code,amout,price):
          self.__user.buy(code, price=price, amount=amout)

trade = Trade()
print(trade.buy('300479',100,18.73))          
