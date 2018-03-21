# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests

class MockTrade(object):
    
      def __init__(self):
          self.__header = {
              'Accept':'application/json, text/javascript, */*; q=0.01',
              'Accept-Encoding':'gzip, deflate',
              'Accept-Language':'zh-CN,zh;q=0.8',
              'Connection':'keep-alive',
              'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
              'Host':'mncg.10jqka.com.cn',
              'Referer':'http://mncg.10jqka.com.cn/cgiwt/index/index',
              'X-Requested-With':'XMLHttpRequest',
              'Cookie':'user=MDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1MjEyNjYyNTA6OjoxNTA2MDQ4OTYwOjYwNDgwMDowOjEwMzEwYzQzYjg3NzE1NjMyZmQ2ZDEwZWZhZmEwNzZiZjpkZWZhdWx0XzI6MQ%3D%3D; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=b0370b40bcc8c0b4f1884c85eb82e1a8; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1521105165,1521633255; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1521633255; v=AoRBWcHygsVZvDYJCfg3AA9EVQlynagHasE8S54lEM8SyS49xq14l7rRDNrt; PHPSESSID=o3dcoqhq0udg20m679n7nk6140; isSaveAccount=0',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
          }

          def mockTrade(code,price,amount):
              postData = {
                 'type' : 'cmd_wt_mairu',
                 'mkcode' : 2,
                 'gdzh' : 'A474614369',
                 'stockcode' : code,
                 'price' : price,
                 'amount' : amount
              }
              return requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/tradestock/',data=postData,headers=header)


