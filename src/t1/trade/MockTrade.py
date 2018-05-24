# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
import time
import json
import datetime as dt
from ..MyLog import MyLog

class MockTrade(object):
    
      def __init__(self):
          self.__header = {
              'Accept':'application/json, text/javascript, */*; q=0.01',
              'Accept-Encoding':'gzip, deflate',
              'Accept-Language':'en-US,en;q=0.9',
              'Connection':'keep-alive',
              'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
              'Host':'mncg.10jqka.com.cn',
              'Referer':'http://mncg.10jqka.com.cn/cgiwt/index/index',
              'X-Requested-With':'XMLHttpRequest',
              'Cookie':'uaid=3e9d33c7f0daebe595757fcd5d3722ba; isSaveAccount=0; searchGuide=sg; historystock=000735%7C*%7C600903%7C*%7C002241%7C*%7C002046%7C*%7C603698; v=AjKEsHj-vUjVWYF0Ye6B6LHZg3MQwzYbaMIqh_wKXuXQj9wl5FOGbThXepnP; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; __utma=156575163.844587348.1519633850.1526893447.1527122480.73; __utmc=156575163; __utmz=156575163.1527122480.73.73.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1526996627,1527036480,1527074138,1527124919; user=MDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1MjcxMjQ5MzQ6OjoxNTA2MDQ4OTYwOjg2NDAwOjA6MTNkY2E1ZjNjZTliZjMzMzI2MDgzODMyN2M1ZjA4NWZmOmRlZmF1bHRfMjox; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=c65cf1034e6a36741d0d082be8dcc937; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=timestamp; PHPSESSID=h2cofv0gi5ljt8f51kuklhd6h1',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
          }

      def relogin(self):
          try:   
             response = requests.get('http://mncg.10jqka.com.cn/cgiwt/login/doths/?type=auto&uname=48039195&password=',headers=self.__header)
             return response.text 
          except Exception as e:
                 MyLog.info('模拟登录失败 e = %s' % e)
                 return ''    

      def mockTrade(self,code,price,amount,tradeType='cmd_wt_mairu'):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          postData = {
              'type' : tradeType,
              'mkcode' : 1,
              'gdzh' : '0098894246',
              'stockcode' : code,
              'price' : price,
              'amount' : amount
          }
          if code.startswith('6'):
             postData['mkcode'] = 2
             postData['gdzh'] = 'A474614369'
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/tradestock/',data=postData,headers=self.__header)
             MyLog.info(response.text)
             j = json.loads(response.text)
             return j['errorcode']
          except Exception as e:
                 MyLog.info('模拟交易失败code = %s,price = %s, amount = %s, e = %s' % (code,price,amount,e))
                 return ''  


      def getHoldStocks(self):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/qryChicang',headers=self.__header)
             return response.text
          except Exception as e:
                 MyLog.info('can not get hold stock')
                 return ''


      def queryDeligated(self):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/qryDelegated',headers=self.__header)
             return response.text
          except Exception as e:
                 MyLog.info('can not get delegate stock')
                 return '' 

      def queryChenjiao(self):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/qryChengjiao',headers=self.__header)
             return response.text
          except Exception as e:
                 MyLog.info('can not get chenjiao stock')
                 return ''          


      def cancelDeligated(self,htbh,wtrq):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))                   
          postData = {
              'htbh' : htbh,
              'wtrq' : wtrq,
          }
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/cancelDelegated/',data=postData,headers=self.__header)
             return response.text
          except Exception as e:
                 MyLog.info('can not cancel deligate')
                 return ''


      def queryBuyStocks(self):
          jsonData = self.queryChenjiao()
          j = json.loads(jsonData)
          stockList = j['result']['list']
          buyCount = 0
          if len(stockList) > 0:
             for stock in stockList:           
                 if stock['d_2109'] == '买入':
                    buyCount = buyCount + 1
          return buyCount     


      def cancelAllBuy(self):
          jsonData = self.queryDeligated()
          j = json.loads(jsonData)
          if 'result' not in j or 'list' not in j['result']:
              return
          stockList = j['result']['list']
          if len(stockList) > 0:
             for stock in stockList:
                 if (int(stock['d_2126']) - int(stock['d_2128'])) > 0 and stock['d_2105'] != '全部撤单' and stock['d_2109'] == '买入':
                    self.cancelDeligated(stock['d_2135'],stock['d_2139'])

      def cancelBuy(self,code):
          jsonData = self.queryDeligated()
          j = json.loads(jsonData)
          if 'result' not in j or 'list' not in j['result']:
              return -1
          stockList = j['result']['list']
          if len(stockList) > 0:
             for stock in stockList:
                 if stock['d_2102'] == code and (int(stock['d_2126']) - int(stock['d_2128'])) > 0 and stock['d_2105'] != '全部撤单' and stock['d_2109'] == '买入':
                    text = self.cancelDeligated(stock['d_2135'],stock['d_2139'])
                    j = json.loads(text)
                    return j['errorcode']
          return -1      


      def sell(self,code,price):
          try:
             isSelled = True
             jsonData = self.queryDeligated()
             j = json.loads(jsonData)
             stockList = j['result']['list']
             if len(stockList) > 0:
                for stock in stockList:
                    if stock['d_2102'] == code and (int(stock['d_2126']) - int(stock['d_2128'])) > 0 and stock['d_2105'] != '全部撤单' and stock['d_2109'] == '卖出':
                        isSelled = False 
                        ct = dt.datetime.strptime(stock['d_2139'] + ' ' + stock['d_2140'], '%Y%m%d %H:%M:%S')
                        if (dt.datetime.now() - ct).seconds > 30: 
                           self.cancelDeligated(stock['d_2135'],stock['d_2139'])
             jsonData = self.getHoldStocks()   
             j = json.loads(jsonData)
             stockList = j['result']['list']
             if len(stockList) > 0:
                for stock in stockList:
                    if stock['d_2102'] == code and int(stock['d_2121']) > 0:
                       isSelled = False 
                       self.mockTrade(code,price,int(stock['d_2121']),tradeType='cmd_wt_maichu') 
             return isSelled
          except Exception as e:
                 MyLog.info('sell [%s] error' % code)
                 return False  
                     
                         

# trade = MockTrade()
# res = trade.relogin()
# MyLog.info(trade.sell('002012',7.68))
# MyLog.info(trade.sell('300191',23.20))
# MyLog.info(trade.sell('300722',46.99))
# MyLog.info(trade.sell('603080',37.04))
# res = trade.mockTrade('300231',10.00,100)
# count = trade.queryBuyStocks()
# MyLog.info(count)


