# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
import time

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
              'Cookie':'v=AoRBWcHygsVZvDYJCfg3AA9EVQlynagHasE8S54lEM8SyS49xq14l7rRDNrt; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; PHPSESSID=h1fjcpenlu7erll0bed9dtmqe2; user=MDptb180MzE1MTk2NzQ6Ok5vbmU6NTAwOjQ0MTUxOTY3NDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA6MjQ6Ojo0MzE1MTk2NzQ6MTUyMjM2NDY1Nzo6OjE1MTUwNjU0MDA6ODY0MDA6MDoxN2EyMGYxNGRkMTNjMzFhMTEyNTBlM2E4ZWZkMmY1N2M6ZGVmYXVsdF8yOjE%3D; userid=431519674; u_name=mo_431519674; escapename=mo_431519674; ticket=4d43a88e10d666c75cefda3533663cdc; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1522191570,1522194475,1522279653,1522364811; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=timestamp; isSaveAccount=0',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
          }

      def relogin(self):
          try:   
             response = requests.get('http://mncg.10jqka.com.cn/cgiwt/login/doths/?type=auto&uname=49403315&password=',headers=self.__header)
             return response.text 
          except Exception as e:
                 print('模拟登录失败 e = %s' % e)
                 return ''    

      def mockTrade(self,code,price,amount):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          postData = {
              'type' : 'cmd_wt_mairu',
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

# trade = MockTrade()
# res = trade.relogin()
# print(res)
# res = trade.mockTrade('300231',10.00,100)
# print(res)


