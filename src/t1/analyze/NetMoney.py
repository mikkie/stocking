# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
import re

class NetMoney(object):
      
      def __init__(self):
          self.__header = {
              'Accept':'*/*',
              'Accept-Encoding':'gzip, deflate',
              'Accept-Language':'en-US,en;q=0.9',
              'Connection':'keep-alive',
              'Content-type':'application/x-www-form-urlencoded',
              'Connection':'keep-alive',
              'Host':'vip.stock.finance.sina.com.cn',
              'Referer':'http://vip.stock.finance.sina.com.cn/moneyflow/',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
          }
          self.__URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_ssggzj?page=1&num=500&sort=ratioamount&asc=0&bankuai=&shichang='

      def getNetMoneyRatio(self):
          try:
             response = requests.get(self.__URL,headers=self.__header, verify=False)
             return self.parse(response.text)
          except:
                print('call top 300 net money failed')
                return None     


      def parse(self,text):
          text = re.subn('sh|sz', '', text)
          res = re.findall('symbol:"(\d{6})"',text[0])
          return res

netMoney = NetMoney()  
netMoney.getNetMoneyRatio()      