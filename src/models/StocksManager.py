# -*-coding=utf-8-*-

__author__ = 'aqua'

from .Stock import Stock 
import numpy as np
import pandas as pd
import talib as ta
import tushare as ts
from sqlalchemy.types import VARCHAR
from ..handlers.StrategyManager import StrategyManager

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
          print(stock)

      def callStrategy(self,stock:Stock,strategy):
          if self.__sm.start(stock.get_code(),strategy,{'df_3m' : stock.get_kdata(),'df_realTime' : stock.get_ktoday(), 'engine' : self.__engine},self.__config) == True:
             return 1
          return 0        

      def buildMACDForStock(self,stock):
          if stock.get_macd() is None:
             stock.set_macd(callStrategy(stock,['macd']))

      def buildKDJForStock(self,stock):
          if stock.get_kdj() is None:
             stock.set_kdj(callStrategy(stock,['kdj'])) 

      def buildTurnoverForStock(self,stock):
          if stock.get_turnover() is None:
             stock.set_turnover(callStrategy(stock,['turnover']))

      def buildVolumeForStock(self,stock):
          if stock.get_volume() is None:
             stock.set_volume(callStrategy(stock,['volume']))

      def buildMAForStock(self,stock):
          if stock.get_ma() is None:
             stock.set_ma(callStrategy(stock,['ma']))

      def buildBigMoneyForStock(self,stock):
          if stock.get_bigMoney() is None:
             stock.set_bigMoney(callStrategy(stock,['bigMoney']))                                  

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
          nprg = self.__dfGrowth.loc[stock.get_code()].get('nprg')
          epsg = self.__dfGrowth.loc[stock.get_code()].get('epsg')
          stock.set_nprg(nprg)
          stock.set_epsg(epsg)   

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
          roe = self.__dfProfit.loc[stock.get_code()].get('roe')
          stock.set_roe(roe)

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
          pe = self.__dfBasic.loc[stock.get_code()].get('pe')  
          pb = self.__dfBasic.loc[stock.get_code()].get('pb')
          esp = self.__dfBasic.loc[stock.get_code()].get('esp')
          bvps = self.__dfBasic.loc[stock.get_code()].get('bvps')
          stock.set_pe(pe)
          stock.set_pb(pb)
          stock.set_esp(esp)
          stock.set_bvps(bvps)
   

      def getStock(self,code):
          return self.__cahce[code]        