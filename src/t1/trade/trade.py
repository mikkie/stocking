# -*-coding=utf-8-*-
__author__ = 'aqua'

import easytrader
import json

class Trade(object):

      def __init__(self):
          self.__user = easytrader.use('ths')
          self.__user.connect(r'C:/xyzqdlxd/xiadan.exe')


      def buy(self,code,amout,price):
          try:
              return self.__user.buy(code, price=price, amount=amout)
          except Exception as e:
                 print('交易失败code = %s,price = %s, amount = %s, e = %s' % (code,price,amout,e))
                 return ''


      def sell(self,code,price):
          isSelled = True
          jsonData = self.__user.today_entrusts
          j = json.loads(jsonData)
                 
          