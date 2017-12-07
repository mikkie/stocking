# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import datetime as dt
import sys
sys.path.append('..')
from utils.Utils import Utils

class MainForceTrendFilter(object):
      pass
      
      def filter(self, data, config):
          df = self.getDataByVol(data,config)
          if self.isInMorethanOut(df,config):
             return True 
          df_amount = self.getDataByAmount(data,config)
          return self.isInMorethanOut(df_amount,config) 

      def isInMorethanOut(self,df,config):
          if df is None or len(df) == 0:
                 return False
          df['total'] = df['price'] * df['volume']
          buy = df.loc[df['type'] == '买盘', 'total'].sum()
          sell = df.loc[df['type'] == '卖盘', 'total'].sum()
          if buy is None or sell is None:
             return False 
          return buy > sell * config.get_BigMoney()[0]


      def getDataByAmount(self,data,config):  
          date = dt.datetime.now().strftime('%Y-%m-%d')
          if not ('df_m_amount' in data) or data['df_m_amount'].empty :
             def cb1(**kw):
                 return ts.get_sina_dd(kw['kw']['code'], date=date,vol=0,amount=config.get_BigMoney()[2])
             data['df_m_amount'] = Utils.queryData('df_m_amount' + data['df_3m'].iloc[0]['code'],'code',data['engine'], cb1, forceUpdate=config.get_updateToday(),code=data['df_3m'].iloc[0]['code'])
          return data['df_m_amount']

      def getDataByVol(self,data,config):
          date = dt.datetime.now().strftime('%Y-%m-%d')
          if not ('df_m' in data) or data['df_m'].empty :
             def cb(**kw):
                 return ts.get_sina_dd(kw['kw']['code'], date=date,vol=config.get_BigMoney()[1])
             data['df_m'] = Utils.queryData('m_data_' + data['df_3m'].iloc[0]['code'],'code',data['engine'], cb, forceUpdate=config.get_updateToday(),code=data['df_3m'].iloc[0]['code'])
          return data['df_m']   
