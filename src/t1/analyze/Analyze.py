# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog

class Analyze(object):
 
      def calcMain(self,dh):
          data = dh.get_data()
          for code in data:
              self.calc(data[code])
              
      def calc(self,stock):
          MyLog.info('=== ' + stock.get_code() + " ===\n")
          MyLog.info(stock.get_data())
                  
              
