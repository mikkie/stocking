# -*-coding=utf-8-*-
__author__ = 'aqua'

class Config(object):

      def __init__(self):
          self.__priceRange = {'min' : 5.00, 'max' : 15.00} #价格区间
          self.__timeStart = '14:25:00' #监控起始时间
          self.__pKm5Change = 0.01 #当日5分钟振幅
          self.__pKM3Change = 0.05 #3个月振幅
          self.__superSold = [0.05,0.2] #超卖
          self.__longPeriod = 180 #半年
          self.__dbUrl = 'mysql://root:aqua@127.0.0.1/stocking?charset=utf8' #数据库地址

      def get_pKm5Change(self):
          return self.__pKm5Change

      def get_SuperSold(self):
          return self.__superSold  

      def get_DBurl(self):
          return self.__dbUrl  


      def get_StartTime(self):
          return self.__timeStart  


      def get_PriceRange(self):
          return self.__priceRange  


      def get_pKM3Change(self):
          return self.__pKM3Change  

      def get_longPeriod(self):
          return self.__longPeriod  

      pass