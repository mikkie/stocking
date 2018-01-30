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
          self.__kLineMA = [10] #K线超过MA5,MA10数量
          self.__volume = [2,2.5] #量的突变
          self.__basics = [2017,3,20,1,5,15,30] #基础过滤
          self.__bigMoney = [1.2,600,300000] #大单净流入
          self.__report = [2017,4] #报告日期
          self.__testCodes = ['300377'] #测试代码
          self.__ignore = ['002839'] #不买的
          self.__conceptCodes = ['000099', '600029', '600115', '600221', '601111','000089', '600004', '600009', '600897','000022', '000088', '000507', '000523', '000659', '002016', '600004', '600325','000592', '000632', '000753', '000905', '600057', '600755', '600897','000652', '000695', '000836', '000897', '000965', '002134', '600082', '600225', '600322', '600583', '600717', '600751', '600821', '600874', '601808', '601919'] #最近题材的股票代码
          self.__topsis = {
              'basics' : {
                  'pe' : 0.07,  #市盈率
                  'pb' : 0.01,  #市净率
                  'esp' : 0.04,  #每股收益率
                  'bvps' : 0.01, #每股净资产
                  'roe' : 0.02, #净资产收益率
                  'nprg' : 0.04, #净利润增长
                  'epsg' : 0.01, #每股收益增长
              },
              'indicator' : {
                   'turnover' : 0.15, #换手率
                   'volume' : 0.15, #成交量
                   'macd' : 0.05, #macd金叉
                   'kdj' : 0.05, #kdj金叉
                   'ma' : 0.1, #均线
                   'bigMoney' : 0.1, #主力资金流入,
                   'concept' : 0.2 #概念题材
              }
          } 
          self.__t1 = {
              'process_num' : 1,
              'stop' : {
                  'am_start' : '09:10:00',
                  'am_stop' : '11:30:00',
                  'pm_start' : '12:55:00',
                  'pm_stop' : '15:00:00',
              },
              'trade' : {
                 'addPrice' : 0.02,
                 'volume' : 500
              },
              'topsis' : {
                  'net' : 0.2,
                  'speed_near' : 0.05,
                  'speed_total' : 0.10,
                  's100' : 0.05,
                  's40' : 0.05,
                  's10' : 0.05,
                  'bigMoney_amount' : 0.15,
                  'bigMoney_volume' : 0.15,
                  'r_break' : 0.2
              },
              'big_money' : {
                  'amount' : 500000,
                  'volume' : 100000
              },
              'get_data_inter' : 1,
              'save_data_inter' : 60,
              'need_recover_data' : False,
              'need_save_data' : True,
              'split_size' : 500,
              'R_line' : {
                  'R1' : 0.191,
                  'R2' : 0.382,
                  'R3' : 0.5,
                  'R4' : 0.618,
                  'R5' : 0.892
              },
              'A' : {
                  'open_p' : [5.0, 10.0],
                  'time' : '10:00:00',
                  'min_R' : 'R2',
                  'speed' : {
                      'near_pos' : 12,
                      'threshold' : 1,
                      'min_single_p' : 0.2
                  },
                  'big_money' : {
                      'single_amount' : 500000,
                      'total_amount' : 8000000,
                      'single_volume' : 100000,
                      'total_volume' : 1500000,
                      'net' : 5000000
                  }
              },
              'B' : {
                  'open_p' : [2.0, 5.0],
                  'time' : '11:00:00',
                  'min_R' : 'R2',
                  'speed' : {
                      'near_pos' : 15,
                      'threshold' : 1.5,
                      'min_single_p' : 0.2
                  },
                  'big_money' : {
                      'single_amount' : 500000,
                      'total_amount' : 10000000,
                      'single_volume' : 100000,
                      'total_volume' : 1800000,
                      'net' : 8000000
                  }
              },
              'C' : {
                  'open_p' : [-1.0, 2.0],
                  'time' : '14:50:00',
                  'min_R' : 'R3',
                  'speed' : {
                      'near_pos' : 30,
                      'threshold' : 2,
                      'min_single_p' : 0.2
                  },
                  'big_money' : {
                      'single_amount' : 500000,
                      'total_amount' : 12000000,
                      'single_volume' : 100000,
                      'total_volume' : 2000000,
                      'net' : 8000000
                  }
              }
          }

      def get_ignore(self):
          return self.__ignore

      def get_t1(self):
          return self.__t1    

      def get_conceptCodes(self):
          return self.__conceptCodes

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