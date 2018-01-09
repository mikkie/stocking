# -*-coding=utf-8-*-

__author__ = 'aqua'

from .Stock import Stock 
import numpy as np
import pandas as pd
import talib as ta
import tushare as ts
from sqlalchemy.types import VARCHAR
import sys
sys.path.append('..')
from handlers.StrategyManager import StrategyManager
import cmath

class StocksManager(object):
      pass

      def __init__(self,engine,config):
          self.__cahce = {}
          self.__engine = engine
          self.__config = config
          self.__sm = StrategyManager()
          self.__dfBasic = None
          self.__dfProfit = None
          self.__dfGrowth = None
          self.__dfData = None

      def addStock(self,stock:Stock):
          self.__cahce[stock.get_code()] = stock
          self.buildBasicsForStock(stock)
          self.buildProfitForStock(stock)
          self.buildGrowthForStock(stock)
          self.buildMACDForStock(stock)
          self.buildKDJForStock(stock)
          self.buildTurnoverForStock(stock)
          self.buildVolumeForStock(stock)
          self.buildMAForStock(stock)
          self.buildBigMoneyForStock(stock)

      def buildDataFrame(self):
          array = []
          index = []
          for code in self.__cahce:
              array.append({'pe' : self.__cahce[code].get_pe(), 'pb' : self.__cahce[code].get_pb(), 'esp' : self.__cahce[code].get_esp(), 'bvps' : self.__cahce[code].get_bvps(), 'roe' : self.__cahce[code].get_roe(), 'nprg' : self.__cahce[code].get_nprg(), 'epsg' : self.__cahce[code].get_epsg(), 'turnover' : self.__cahce[code].get_turnover(), 'volume' :  self.__cahce[code].get_volume(), 'macd' : self.__cahce[code].get_macd(), 'kdj' : self.__cahce[code].get_kdj(), 'ma' : self.__cahce[code].get_ma(), 'bigMoney' : self.__cahce[code].get_bigMoney()})    
              index.append(code)    
          self.__dfData = pd.DataFrame(array,index=index)
          if self.__dfData.empty:
             return self.__dfData 
          self.calc()
          return self.__dfData 


      def commonCalc(self,columnName,weight,positive):
          temp = cmath.sqrt((self.__dfData[columnName] * self.__dfData[columnName]).sum())  
          #wi*ri
          if temp == 0:
             self.__dfData[columnName + '_vi'] = weight * 0
          else:
             self.__dfData[columnName + '_vi'] = weight * self.__dfData[columnName] / temp
          #vi+, vi-
          if positive == True:
             self.__dfData[columnName + '_best'] = self.__dfData[columnName + '_vi'].max()
             self.__dfData[columnName + '_worst'] = self.__dfData[columnName + '_vi'].min()
          else:          
             self.__dfData[columnName + '_best'] = self.__dfData[columnName + '_vi'].min()
             self.__dfData[columnName + '_worst'] = self.__dfData[columnName + '_vi'].max()


      def calcDi(self,index,row,columnList,best_worst):
          temp = 0
          for column in columnList:
              temp = temp + np.square(row[column + '_vi'] - row[column + best_worst])
          row['Di' + best_worst] = cmath.sqrt(temp)
          self.__dfData.loc[index,'Di' + best_worst] = row['Di' + best_worst]

      def calcCi(self,index,row):
          if (row['Di_best'] + row['Di_worst']) == 0:
             row['ci'] = 0 
             self.__dfData.loc[index,'ci'] = 0
          else:    
             row['ci'] = row['Di_worst'] / (row['Di_best'] + row['Di_worst'])  
             self.__dfData.loc[index,'ci'] = row['ci']         

      def calc(self):
          self.__dfData = self.__dfData.fillna(self.__dfData.mean())
          self.commonCalc('pe',self.__config.get_topsis()['basics']['pe'],False)
          self.commonCalc('pb',self.__config.get_topsis()['basics']['pb'],False)
          self.commonCalc('esp',self.__config.get_topsis()['basics']['esp'],True)
          self.commonCalc('bvps',self.__config.get_topsis()['basics']['bvps'],True)
          self.commonCalc('nprg',self.__config.get_topsis()['basics']['nprg'],True)
          self.commonCalc('epsg',self.__config.get_topsis()['basics']['epsg'],True)
          self.commonCalc('roe',self.__config.get_topsis()['basics']['roe'],True)
          self.commonCalc('turnover',self.__config.get_topsis()['indicator']['turnover'],True)
          self.commonCalc('volume',self.__config.get_topsis()['indicator']['volume'],True)
          self.commonCalc('ma',self.__config.get_topsis()['indicator']['ma'],True)
          self.commonCalc('macd',self.__config.get_topsis()['indicator']['macd'],True)
          self.commonCalc('kdj',self.__config.get_topsis()['indicator']['kdj'],True)
          self.commonCalc('bigMoney',self.__config.get_topsis()['indicator']['bigMoney'],True)
          for index,row in self.__dfData.iterrows():
              self.calcDi(index,row,['pe','pb','esp','bvps','nprg','epsg','roe','turnover','volume','ma','macd','kdj','bigMoney'],'_best')
              self.calcDi(index,row,['pe','pb','esp','bvps','nprg','epsg','roe','turnover','volume','ma','macd','kdj','bigMoney'],'_worst')
              self.calcCi(index,row) 
          self.__dfData = self.__dfData.sort_values('ci',ascending=False)    


      def callStrategy(self,stock:Stock,strategy):
          if self.__sm.start(stock.get_code(),strategy,{'df_3m' : stock.get_kdata(),'df_realTime' : stock.get_ktoday(), 'engine' : self.__engine},self.__config) == True:
             return 1
          return 0        

      def buildMACDForStock(self,stock):
          if stock.get_macd() is None:
             stock.set_macd(self.callStrategy(stock,['macd']))

      def buildKDJForStock(self,stock):
          if stock.get_kdj() is None:
             stock.set_kdj(self.callStrategy(stock,['kdj'])) 

      def buildTurnoverForStock(self,stock):
          if stock.get_turnover() is None:
             stock.set_turnover(self.callStrategy(stock,['turnover']))

      def buildVolumeForStock(self,stock):
          if stock.get_volume() is None:
             stock.set_volume(self.callStrategy(stock,['volume']))

      def buildMAForStock(self,stock):
          if stock.get_ma() is None:
             stock.set_ma(self.callStrategy(stock,['ma']))

      def buildBigMoneyForStock(self,stock):
          if stock.get_bigMoney() is None:
             stock.set_bigMoney(self.callStrategy(stock,['bigMoney']))                                  

      def buildGrowthForStock(self,stock): 
          code = stock.get_code()
          if self.__dfGrowth is None or self.__dfGrowth.empty:
             try:
                 self.__dfGrowth = pd.read_sql_table('growth', con=self.__engine, index_col='code')
             except:
                 pass 
             if self.__dfGrowth is None or self.__dfGrowth.empty:
                self.__dfGrowth = ts.get_growth_data(self.__config.get_report()[0],self.__config.get_report()[1])
                self.__dfGrowth.to_sql('growth',self.__engine,if_exists='replace',index_label='code',index=False)     
          try:
             nprg = self.__dfGrowth.loc[stock.get_code()].get('nprg')
             if isinstance(nprg,pd.Series):
                nprg = nprg.iat[-1] 
             epsg = self.__dfGrowth.loc[stock.get_code()].get('epsg')
             if isinstance(epsg,pd.Series):
                epsg = epsg.iat[-1] 
             stock.set_nprg(nprg)
             stock.set_epsg(epsg)   
          except:
              stock.set_nprg(float("nan"))
              stock.set_epsg(float("nan"))

      def buildProfitForStock(self,stock):
          code = stock.get_code()
          if self.__dfProfit is None or self.__dfProfit.empty:
             try:
                 self.__dfProfit = pd.read_sql_table('profit', con=self.__engine, index_col='code')
             except:
                 pass 
             if self.__dfProfit is None or self.__dfProfit.empty:
                self.__dfProfit = ts.get_profit_data(self.__config.get_report()[0],self.__config.get_report()[1])
                self.__dfProfit.to_sql('profit',self.__engine,if_exists='replace',index_label='code',index=False)     
          try:
             roe = self.__dfProfit.loc[stock.get_code()].get('roe')
             if isinstance(roe,pd.Series):
                roe = roe.iat[-1] 
             stock.set_roe(roe)
          except:
             stock.set_roe(float("nan")) 
                     

      def buildBasicsForStock(self,stock):
          code = stock.get_code()
          if self.__dfBasic is None or self.__dfBasic.empty:
             try:
                 self.__dfBasic = pd.read_sql_table('basics', con=self.__engine, index_col='code')
             except:
                 pass 
             if self.__dfBasic is None or self.__dfBasic.empty:
                self.__dfBasic = ts.get_stock_basics() 
                self.__dfBasic.to_sql('basics',self.__engine,if_exists='replace',index_label='code',dtype={'code': VARCHAR(self.__dfBasic.index.get_level_values('code').str.len().max())})   
          try:
             pe = self.__dfBasic.loc[stock.get_code()].get('pe')  
             pb = self.__dfBasic.loc[stock.get_code()].get('pb')
             esp = self.__dfBasic.loc[stock.get_code()].get('esp')
             bvps = self.__dfBasic.loc[stock.get_code()].get('bvps')
             stock.set_pe(pe)
             stock.set_pb(pb)
             stock.set_esp(esp)
             stock.set_bvps(bvps)
          except:
             stock.set_pe(float("nan"))
             stock.set_pb(float("nan"))
             stock.set_esp(float("nan"))
             stock.set_bvps(float("nan"))
                    
   

      def getStock(self,code):
          return self.__cahce[code]        