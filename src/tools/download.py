# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests

dls = "http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=%s&d=%s"
date = '20180919'
stocks = [('300013','8.45')]
headers = {
   'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Host' : 'stock.gtimg.cn',
   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}

for stock in stocks:
    if stock[0].startswith('6'):
       code = 'sh' + stock[0]
    else:
        code = 'sz' + stock[0]    
    resp = requests.get(dls % (code, date), headers=headers)
    output = open('D:/aqua/stock/stocking/data/excels/%s%s.xls' % (code + stock[1], date), 'wb')
    output.write(resp.content)
    output.close()