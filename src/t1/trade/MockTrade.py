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
              'Cookie':'uaid=3e9d33c7f0daebe595757fcd5d3722ba; historystock=603778%7C*%7C000909%7C*%7C600728%7C*%7C002208%7C*%7C000727; isSaveAccount=0; v=AhOlnxE1TYZNJgHSlcKWB5nLopw5yKd5YUHrk8UxbWBrBD3KTZg32nEsexDW; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; __utma=156575163.844587348.1519633850.1522049794.1522284292.30; __utmc=156575163; __utmz=156575163.1522284292.30.30.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; __utmt=1; __utmb=156575163.1.10.1522284292; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1522235330,1522278321,1522284151,1522284295; user=MDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1MjIyODQzMTA6OjoxNTA2MDQ4OTYwOjg2NDAwOjA6MWE2NWZmNGU1YTU1MGQwYzY2OWQwMjc0YjkyNTg0YTE1OmRlZmF1bHRfMjox; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=72463532ce1d85ca3a362dfff693e584; PHPSESSID=v9ktvttvfnr9fr172rp7a07ed5; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=timestamp',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
          }

      def relogin(self):
          try:   
             response = requests.get('http://mncg.10jqka.com.cn/cgiwt/login/doths/?type=auto&uname=48039195&password=',headers=self.__header)
             return response.text 
          except Exception as e:
                 print('模拟登录失败 e = %s' % e)
                 return ''    

      def mockTrade(self,code,price,amount):
          self.__header['Cookie'] = self.__header['Cookie'].replace('timestamp',str(time.time()))
          postData = {
              'type' : 'cmd_wt_mairu',
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
             return response.text
          except Exception as e:
                 print('模拟交易失败code = %s,price = %s, amount = %s, e = %s' % (code,price,amount,e))
                 return ''  

# trade = MockTrade()
# res = trade.relogin()
# print(res)
# res = trade.mockTrade('300231',10.00,100)
# print(res)


