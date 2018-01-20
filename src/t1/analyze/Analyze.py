# -*-coding=utf-8-*-
__author__ = 'aqua'


class Analyze(object):
 
      def calcMain(self,dh):
          data = dh.get_data()
          for code in data:
              self.calc(data[code])
              
      def calc(self,stock):
          print('=== ' + stock.get_code() + " ===\n")
          print('=== ' + stock.get_data() + " ===")
                  
              
