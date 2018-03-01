# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
from lxml import etree

class Concept(object):
      
      def __init__(self):
          self.__header = {
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding':'gzip, deflate', 
              'Accept-Language':'en-US,en;q=0.9',
              'Cache-Control':'max-age=0',
              'Connection':'keep-alive',
              'Host':'data.10jqka.com.cn',
              'Referer':'http://q.10jqka.com.cn/',
              'Upgrade-Insecure-Requests':'1',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
          }
          self.__hyURL = 'http://data.10jqka.com.cn/funds/hyzjl/'
          self.__gnURL = 'http://data.10jqka.com.cn/funds/gnzjl/'

      def getCurrentTopHYandConcept(self):
          try:
              response = requests.get(self.__hyURL,headers=self.__header, verify=False)
              hyNames = self.parse(response.text)
              response = requests.get(self.__gnURL,headers=self.__header, verify=False)
              gnNames = self.parse(response.text)
              return {'hy' : hyNames,'gn' : gnNames}
          except:
              print('call top 6 concept failed')
              return None

                  


      def parse(self,html):
          names = []
          page = etree.HTML(html)
          trs = page.xpath('//table[@class="m-table J-ajax-table"]/tbody/tr')
          i = 0
          while i < 6:
                name = trs[i].getchildren()[1].getchildren()[0].text
                names.append(name)
                i = i + 1
          return names

concept = Concept()  
concept.getCurrentTopHYandConcept()      