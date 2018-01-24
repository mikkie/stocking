# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog
import sys
sys.path.append('../..')
from config.Config import Config 

class Analyze(object):
    
      def __init__(self):
          self.__config = Config()
 
      def calcMain(self,dh):
          data = dh.get_data()
          for code in data:
              self.calc(data[code])
              
      def calc(self,stock):
          MyLog.info('=== ' + stock.get_code() + " ===\n")
          MyLog.info(stock.get_data())
          if not self.canCalc(stock):
             return False 
          open_p = self.getOpenPercent(stock)
          conf = self.getConfig(open_p)  
          self.initStockData(stock,open_p,conf)
          self.updateStock(stock,conf)  
          return self.isStockMatch(stock,conf)   


      def canCalc(self,stock):
          if stock.len() < 0:
             return False
          lastLine = stock.get_Lastline() 
          if lastLine.get('open') == 0.0:
             return False
          lastSecondLine = stock.get_LastSecondline() 
          if lastSecondLine.get('open') == 0.0:
             return False    
          return True     


      def initStockData(self,stock,open_p,conf):
          r_line = self.__config.get_t1()['R_line']
          for key in r_line:
              val = open_p + (10 - open_p) * r_line[key]
              stock.set_r_val(key,val)


      def updateStock(self,stock,conf):
          self.updateBreakRtimes(stock,conf)
          self.updateSpeedCount(stock,conf)
          self.updateBigMoney(stock,conf)



      def updateSpeedCount(self,stock,conf):
          data = stock.get_data()
          last_line = data.iloc[-1]
          pre_pos = conf['speed']['near_pos']
          if pre_pos > stock.len():
             pre_pos = stock.len() 
          df_temp = data.tail(pre_pos)
          for index,row in df_temp.iterrows():
              if row['open'] != 0:
                 p = (float(last_line.get('price')) - float(row['price'])) / float(row['open']) * 100 
                 stock.set_near_speed(p)
                 break
          last_second_line = data.iloc[-2]
          p = (float(last_line.get('price')) - float(last_second_line.get('price'))) / float(last_line.get('open')) * 100 
          if p > conf['speed']['min_single_p']:
             stock.add_total_speed(p)      


      def theLastIsSellOrBuy(self,stock):
          lastLine = stock.get_Lastline()
          lastSeconfLine = stock.get_LastSecondline()


      def updateBigMoney(self,stock,conf):
          pass
             


                  

          


      def updateBreakRtimes(self,stock,conf):
          now_p = self.getCurrentPercent(stock)
          lastSecondLine = stock.get_LastSecondline()
          last_p = self.getPercent(lastSecondLine.get('price'),stock)
          for key in ['R1','R2','R3','R4','R5']:
              val = stock.get_r_val(key)
              if last_p > val and now_p < val:
                 stock.add_rBreakTimes(key) 



      def getConfig(self,open_p):
          t1 = self.__config.get_t1()
          keys = ['A','B','C','D']
          for key in keys:
              if t1[key]['open_p'][0] and open_p < t1[key]['open_p'][1]:
                 return t1[key] 

      def isStockMatch(self,stock,conf):
          pass


      def getPercent(self,price,stock):
          lastLine = stock.get_Lastline()
          pre_close = lastLine.get('pre_close') 
          open_p = (price - pre_close) / pre_close * 100
          return open_p
      
      def getCurrentPercent(self,stock):
          lastLine = stock.get_Lastline()
          price = lastLine.get('price')
          return self.getPercent(price,stock)
              

      def getOpenPercent(self,stock):
          lastLine = stock.get_Lastline()
          open = lastLine.get('open')
          return self.getPercent(open,stock)  


      def isReachMinR(self,stock,conf):
          r_line = self.__config.get_t1()['R_line'] 
          ratio = r_line[conf['min_R']]
          open_p = self.getCurrentPercent(stock)
          return self.getCurrentPercent(stock) > open_p + (10 - open_p) * ratio

              


              
