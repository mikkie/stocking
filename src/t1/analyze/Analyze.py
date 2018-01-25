# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog
import datetime as dt
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
          last_amount = float(lastLine.get('amount'))
          last_sec_amount = float(lastSeconfLine.get('amount'))
          if last_sec_amount == last_amount:
             return 'no_deal' 
          last_price = float(lastLine.get('price'))  
          last_b_p_1 = float(lastLine.get('b1_p'))
          last_b_v_1 = float(lastLine.get('b1_v'))
          last_a_p_1 = float(lastLine.get('a1_p'))
          last_a_v_1 = float(lastLine.get('a1_v'))
          last_sec_price = float(lastSeconfLine.get('price'))
          last_sec_b_p_1 = float(lastSeconfLine.get('b1_p'))
          last_sec_b_v_1 = float(lastSeconfLine.get('b1_v'))
          last_sec_a_p_1 = float(lastSeconfLine.get('a1_p'))
          last_sec_a_v_1 = float(lastSeconfLine.get('a1_v'))
          if (last_a_p_1 > last_sec_a_p_1 or (last_a_p_1 == last_sec_a_p_1 and last_a_v_1 < last_sec_a_v_1)) and (last_price >= last_sec_price):
             return 'drive_buy'
          elif (last_b_p_1 < last_sec_b_p_1 or (last_b_p_1 == last_sec_b_p_1 and last_b_v_1 < last_sec_b_v_1)) and (last_price <= last_sec_price):
             return 'drive_sell'
          return 'unknown'       


      def updateBigMoney(self,stock,conf):
          lastLine = stock.get_Lastline()
          lastSeconfLine = stock.get_LastSecondline()
          last_amount = float(lastLine.get('amount'))
          last_sec_amount = float(lastSeconfLine.get('amount'))
          last_volume = float(lastLine.get('volume'))
          last_sec_volume = float(lastSeconfLine.get('volume'))
          amount = last_amount - last_sec_amount
          volume = last_volume - last_sec_volume
          if amount >= conf['big_money']['single_amount']:
             stock.addBigMoneyTotalAmount(amount)
          if volume >= conf['big_money']['single_volume']:
             stock.addBigMoneyTotalVolume(volume) 
          type = self.theLastIsSellOrBuy(stock)
          if type == 'drive_buy':
             stock.addNetBuy(last_amount - last_sec_amount)  
          elif type == 'drive_sell':
             stock.addNetBuy(last_sec_amount - last_amount)           

             
      def updateBreakRtimes(self,stock,conf):
          now_p = self.getCurrentPercent(stock)
          lastSecondLine = stock.get_LastSecondline()
          last_p = self.getPercent(lastSecondLine.get('price'),stock)
          for key in ['R1','R2','R3','R4','R5']:
              val = stock.get_r_val(key)
              if last_p > val and now_p < val:
                 stock.add_rBreakTimes(key) 
          minR = conf['min_R']
          if stock.get_rBreakTimes(minR) > 0:
             for i in [1,2,3,4,5]:
                 if i > int(minR[-1]) and stock.get_rBreakTimes('R' + i) == 0:
                    stock.set_minR('R' + i)        
          else:
              stock.set_minR(minR)



      def getConfig(self,open_p):
          t1 = self.__config.get_t1()
          keys = ['A','B','C','D']
          for key in keys:
              if t1[key]['open_p'][0] and open_p < t1[key]['open_p'][1]:
                 return t1[key] 

      def isStockMatch(self,stock,conf):
          if not self.isTimeMatch(conf):
             return False
          if not self.isReachMinR(stock):
             return False
          if not self.isNetMatch(stock,conf):
             return False      
          if stock.get_minR() != 'R5':
             if not self.isPeedMatch(stock,conf) and not self.isBigMoneyMatch(stock,conf):
                return False 
          return self.isLastTwoMatch(stock)


      def isLastTwoMatch(self,stock):
          now_p = self.getCurrentPercent(stock)
          lastSecondLine = stock.get_LastSecondline()
          last_p = self.getPercent(lastSecondLine.get('price'),stock)
          return now_p > 0 and last_p >= 0
          


      def isPeedMatch(self,stock,conf):
          stock.get_near_speed() >= conf['speed']['threshold'] or stock.get_total_speed() >= conf['speed']['threshold']


      def isBigMoneyMatch(self,stock,conf):
          stock.getBigMoneyTotalAmount() >= conf['big_money']['total_amount'] or stock.getBigMoneyTotalVolume() >= conf['big_money']['total_volume']


      def isNetMatch(self,stock):
          return stock.get_net() >= conf['big_money']['net']



      def isTimeMatch(self,conf):
          now = dt.datetime.now()
          timeStr = now.strftime('%H:%M:%S')
          return timeStr <= conf['time']


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


      def isReachMinR(self,stock):
          now_p = self.getCurrentPercent(stock)
          minR = stock.get_minR()
          return now_p > stock.get_r_val(minR)

              


              
