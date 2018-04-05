# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
import time
import json
import datetime as dt

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
              'Cookie':'historystock=002076; spversion=20130314; v=Au4rHwcgOBiZ9Ux8JgV93hGWP0-077LKxLBmzRi2WvGs-4T7gH8C-ZRDttjr; user=MDptb180MzE1MTk2NzQ6Ok5vbmU6NTAwOjQ0MTUxOTY3NDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA6MjQ6Ojo0MzE1MTk2NzQ6MTUyMjcwOTg2Mjo6OjE1MTUwNjU0MDA6ODY0MDA6MDoxZWUxNDJhMDI1NzU2MGZlNzEzOThhYTQ4Y2IwZDlhMWM6ZGVmYXVsdF8yOjE%3D; userid=431519674; u_name=mo_431519674; escapename=mo_431519674; ticket=10315524db445cbb849c63224061a8aa; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1522364811,1522453671,1522622743,1522709835; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=timestamp; PHPSESSID=3p8qkjatdc60qe36oumelran34; isSaveAccount=0',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
          }

      def relogin(self):
          try:   
             response = requests.get('http://mncg.10jqka.com.cn/cgiwt/login/doths/?type=auto&uname=49403315&password=',headers=self.__header)
             return response.text 
          except Exception as e:
                 print('模拟登录失败 e = %s' % e)
                 return ''    

      def mockTrade(self,code,price,amount,tradeType='cmd_wt_mairu'):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          postData = {
              'type' : tradeType,
              'mkcode' : 1,
              'gdzh' : '00100258366',
              'stockcode' : code,
              'price' : price,
              'amount' : amount
          }
          if code.startswith('6'):
             postData['mkcode'] = 2
             postData['gdzh'] = 'A475978489'
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/tradestock/',data=postData,headers=self.__header)
             return response.text
          except Exception as e:
                 print('模拟交易失败code = %s,price = %s, amount = %s, e = %s' % (code,price,amount,e))
                 return ''  


      def getHoldStocks(self):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/qryChicang',headers=self.__header)
             return response.text
          except Exception as e:
                 print('can not get hold stock')
                 return ''


      def queryDeligated(self,code):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          postData = {
              'gdzh' : '0098894246',
              'mkcode' : 1,
          }
          if code.startswith('6'):
             postData['mkcode'] = 2
             postData['gdzh'] = 'A474614369'
          try:   
             response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/qryDelegated',data=postData,headers=self.__header)
             return response.text
          except Exception as e:
                 print('can not get hold stock')
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
                 print('can not get hold stock')
                 return '' 


      def sell(self,code,price):
          isSelled = True
          jsonData = self.queryDeligated(code)
          j = json.loads(jsonData)
          stockList = j['result']['list']
          if len(stockList) > 0:
             for stock in stockList:
                 if stock['d_2102'] == code and (int(stock['d_2126']) - int(stock['d_2128'])) > 0 and stock['d_2105'] != '全部撤单':
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
                     
                         

trade = MockTrade()
res = trade.relogin()
# print(trade.sell('002012',7.68))
# print(trade.sell('300191',23.20))
# print(trade.sell('300722',46.99))
# print(trade.sell('603080',37.04))
# res = trade.mockTrade('300231',10.00,100)
# print(res)


