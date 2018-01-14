# -*-coding=utf-8-*-
__author__ = 'aqua'

class Calculate(object):
      pass

      def calc(self,codeList,dh):
          for code in codeList:
              df = dh.get_data(code)
              self.handle(code,df)
          
      def handle(self,code,df):
          print(code)
          print(df)    