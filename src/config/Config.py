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
          self.__trendPeriod = 180 #主要分析范围 最近120天
          self.__dbUrl = 'mysql://root:aqua@127.0.0.1/stocking?charset=utf8' #数据库地址
          self.__turnOver = 3.00 #换手率
          self.__updateToday = True #更新当前实时价格
          self.__strategy = ['turnover','rightTrade'] #使用策略
          self.__kLineMA = [3,1,1] #K线超过MA5,MA10数量的百分比
          self.__volume = [3,15,1.3,1.5] #量的突变
          self.__basics = [2017,3,20,1,5,15,30] #基础过滤
          self.__bigMoney = [1.2,600,300000] #大单净流入
          self.__report = [2017,4] #报告日期
          self.__testCodes = ['000738','000717'] #测试代码
          self.__topsis = {
              'basics' : {
                  'pe' : 0.08,  #市盈率
                  'pb' : 0.02,  #市净率
                  'esp' : 0.06,  #每股收益率
                  'bvps' : 0.02, #每股净资产
                  'roe' : 0.04, #净资产收益率
                  'nprg' : 0.06, #净利润增长
                  'epsg' : 0.02, #每股收益增长
              },
              'indicator' : {
                   'turnover' : 0.15, #换手率
                   'volume' : 0.1, #成交量
                   'macd' : 0.125, #macd金叉
                   'kdj' : 0.125, #kdj金叉
                   'ma' : 0.05, #均线
                   'bigMoney' : 0.15, #主力资金流入
              }
          } 


      def get_report(self):
          return self.__report

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


      def get_Volume(self):
          return self.__volume  

      def get_Basic(self):
          return self.__basics 

      def get_BigMoney(self):
          return self.__bigMoney

      def get_TestCodes(self):
          return self.__testCodes

      def get_topsis(self):
          return self.__topsis  

      pass