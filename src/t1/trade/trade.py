# -*-coding=utf-8-*-
__author__ = 'aqua'

import easytrader

class Trade(object):

      def __init__(self):
          self.__user = easytrader.use('ths')
          self.__user.connect(r'C:/Users/benjaminl/AppData/Roaming/VOS/AppName.16346')


      def buy(self,code,amout,price):
          self.__user.buy(code, price=price, amount=amout)

trade = Trade()
trade.buy('601965',8.3,500)          
