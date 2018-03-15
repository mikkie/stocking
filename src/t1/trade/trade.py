# -*-coding=utf-8-*-
__author__ = 'aqua'

import easytrader

class Trade(object):

      def __init__(self):
          self.__user = easytrader.use('ths')
          self.__user.connect(r'C:/xyzqdlxd/xiadan.exe')


      def buy(self,code,amout,price):
          try:
              self.__user.buy(code, price=price, amount=amout)
          except Exception as e:
                 print('交易失败code = %s,price = %s, amount = %s, e = %s' % (code,price,amout,e))
          