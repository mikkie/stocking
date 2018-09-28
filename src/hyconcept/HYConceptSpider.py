# -*-coding=utf-8-*-
__author__ = 'aqua'

import time
import random
import requests
from HYConceptParser import HYConceptParser

header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'uaid=3e9d33c7f0daebe595757fcd5d3722ba; searchGuide=sg; spversion=20130314; historystock=000610%7C*%7C000593%7C*%7C603706%7C*%7C002806%7C*%7C300069; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; __utma=156575163.844587348.1519633850.1537925917.1538122047.118; __utmc=156575163; __utmz=156575163.1538122047.118.118.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1537341480,1537852532,1537925932,1538122050; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1538122064; v=ArEHtYeDTu3WyeL56HGCpHDKwDZIniUQzxLJJJPGrXiXut8g2-414F9i2fYg',
        'Host':'q.10jqka.com.cn',
        'Referer':'http://q.10jqka.com.cn/thshy/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }

codes = [];
hy = ['881166','881163']
gn = ['301780']
hyURL = 'http://q.10jqka.com.cn/thshy/detail/code/'
gnURL = 'http://q.10jqka.com.cn/gn/detail/code/' 
gnURL2 = 'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/%s/ajax/1/code/'



def parsePage(parser, html):
    temps = parser.parse(html)
    for temp in temps:
        if temp not in codes:
           codes.append(temp)

def func(url,url2,hygnList):
    parser = HYConceptParser()
    for code in hygnList:
        response = requests.get(url + code+'/',headers=header, verify=False)
        total_page = parser.get_page_info(response.text)
        parsePage(parser, response.text)
        if total_page > 1:
           for i in range(2, total_page + 1):
               time.sleep(random.randint(10,15))
               response = requests.get((url2 % i) + code+'/',headers=header, verify=False)   
               parsePage(parser, response.text)  

# func(hyURL,hy)
func(gnURL,gnURL2,gn)    
print(codes)

