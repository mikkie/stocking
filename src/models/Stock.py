# -*-coding=utf-8-*-

__author__ = 'aqua'

class Stock(object):
      pass
      
      def __init__(self, code):
          self.__code = code

      def get_code(self):
          return self.__code

      def set_kdata(self,kdata):
          self.__kdata = kdata  

      def get_kdata(self):
          return self.__kdata    

      def set_ktoday(self,ktoday):
          self.__ktoday = ktoday  

      def get_ktoday(self):
          return self.__ktoday      

      def set_pe(self,pe):
          self.__pe = pe

      def set_pb(self,pb):
          self.__pb = pb

      def set_esp(self,esp):
          self.__esp = esp

      def set_bvps(self,bvps):
          self.__bvps = bvps

      def set_roe(self,roe):
          self.__roe = roe

      def set_nprg(self,nprg):
          self.__nprg = nprg

      def set_epsg(self,epsg):
          self.__epsg = epsg

      def set_turnover(self,turnover):
          self.__turnover = turnover

      def get_turnover(self):
          return self.__turnover    

      def set_volume(self,volume):
          self.__volume = volume

      def get_volume(self):
          return self.__volume    

      def set_macd(self,macd):
          self.__macd = macd

      def get_macd(self):
          return self.__macd    

      def set_kdj(self,kdj):
          self.__kdj = kdj

      def get_kdj(self):
          return self.__kdj    

      def set_ma(self,ma):
          self.__ma = ma

      def get_ma(self):
          return self.__ma    

      def set_bigMoney(self,bigMoney):
          self.__bigMoney = bigMoney  

      def get_bigMoney(self):
          return self.__bigMoney                                                   


