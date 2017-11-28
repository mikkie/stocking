# -*-coding=utf-8-*-
__author__ = 'aqua'

class Config(object):

      def __init__(self):
          self.__priceRange = {'min' : 3.00, 'max' : 30.00} #价格区间
          self.__timeStart = '14:25:00' #监控起始时间
          self.__pKm5Change = 0.01 #当日5分钟振幅
          self.__pKM3Change = 0.05 #3个月振幅
          self.__superSold = [0.05,0.2] #超卖
          self.__leftTrade = [5,4,3] #左侧交易
          self.__flatTrade = [90, 10, 1.2, 1.5] #长时间横盘后突破
          self.__longPeriod = 365 #1年
          self.__trendPeriod = 180 #主要分析范围 最近180天
          self.__dbUrl = 'mysql://root:aqua@127.0.0.1/stocking?charset=utf8' #数据库地址
          self.__turnOver = 3.00 #换手率
          self.__updateToday = False #更新当前实时价格
          self.__strategy = ['turnover','rightTrade','macd'] #使用策略
          self.__kLineMA = [0.8,0.6] #K线超过MA5,MA10数量的百分比

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

      def get_TurnOver(self):
          return self.__turnOver  

      def get_LeftTrade(self):
          return self.__leftTrade

      def get_updateToday(self):
          return self.__updateToday

      def get_trendPeriod(self):
          return self.__trendPeriod  

      def get_Strategy(self):
          return self.__strategy 

      def get_KLineMA(self):
          return self.__kLineMA   


      def get_FlatTrade(self):
          return self.__flatTrade  

      pass