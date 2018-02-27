# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
from HYConceptParser import HYConceptParser

header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'uaid=3e9d33c7f0daebe595757fcd5d3722ba; spversion=20130314; historystock=002650%7C*%7C300033; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1519633826,1519692417; __utma=156575163.844587348.1519633850.1519633850.1519692420.2; __utmc=156575163; __utmz=156575163.1519692420.2.2.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1519692494; v=Aqge3lYMZt8hk0pb095tdgYSeZ2-0Qzb7jXgX2LZ9CMWvUYLCuHcaz5FsOex',
        'Host':'q.10jqka.com.cn',
        'Referer':'http://q.10jqka.com.cn/thshy/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
response = requests.get('http://q.10jqka.com.cn/thshy/detail/code/881163/',headers=header, verify=False)
parser = HYConceptParser()
parser.parse(response.text)
