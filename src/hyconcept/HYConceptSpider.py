# -*-coding=utf-8-*-
__author__ = 'aqua'

import time
import random
import requests
import re
import pandas as pd
from sqlalchemy import create_engine
import random
from HYConceptParser import HYConceptParser

header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'uaid=3e9d33c7f0daebe595757fcd5d3722ba; searchGuide=sg; spversion=20130314; historystock=000610%7C*%7C000593%7C*%7C603706%7C*%7C002806%7C*%7C300069; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; __utma=156575163.844587348.1519633850.1538122047.1538182476.119; __utmc=156575163; __utmz=156575163.1538182476.119.119.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1537852532,1537925932,1538122050,1538182486; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1538198127; vvvv=1; v=AoI0oCgObfJXw3Euww9B6acv04PnU4ZtOFd6kcybrvWgHyy1tOPWfQjnyqCf',
        'Host':'q.10jqka.com.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }


header_gn_main = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'uaid=3e9d33c7f0daebe595757fcd5d3722ba; searchGuide=sg; spversion=20130314; historystock=000610%7C*%7C000593%7C*%7C603706%7C*%7C002806%7C*%7C300069; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; __utma=156575163.844587348.1519633850.1538122047.1538182476.119; __utmc=156575163; __utmz=156575163.1538182476.119.119.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; __utmb=156575163.1.10.1538182476; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1537852532,1537925932,1538122050,1538182486; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1537925933,1538122050,1538122060,1538182486; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1537925932,1538122050,1538122060,1538182487; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1538183376; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1538183376; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1538183377; v=AvBG9s7kX111XANZSYLzN7k1wbVBOdSD9h0oh-pBvMsepZ5jkkmkE0Yt-BY5',
    'Host': 'data.10jqka.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}    

engine = create_engine('mysql://root:aqua@127.0.0.1/stocking?charset=utf8')
hy = ['881166','881163']
gn = [('http://q.10jqka.com.cn/gn/detail/code/301497/','啤酒'),('http://q.10jqka.com.cn/gn/detail/code/301402/','上海国资改革'),('http://q.10jqka.com.cn/gn/detail/code/302027/','电子竞技'),('http://q.10jqka.com.cn/gn/detail/code/300777/','稀缺资源'),('http://q.10jqka.com.cn/gn/detail/code/302131/','智能音箱')]
hyURL = 'http://q.10jqka.com.cn/thshy/detail/code/'
gn_main_url = 'http://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/%s/ajax/1/'
failed_gn_main_url = []
gnURL = 'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/%s/ajax/1/code/'



def parsePage(parser, html, url, concept, exists_df):
    temps = parser.parse(html)
    if len(temps) == 0:
       print("('%s','%s')" % (url, concept)) 
    codelist = []  
    for temp in temps:
        code_obj = {
            'code' : temp,
            'concept' : concept
        }
        match_df = exists_df[(exists_df['code'] == temp) & (exists_df['concept'] == concept)]
        if len(match_df) == 0:
           codelist.append(code_obj)
    df = pd.DataFrame(codelist) 
    df.to_sql('ths_concept', con=engine, if_exists='append', index=False)   



def main_page(failed_gn_main_url=failed_gn_main_url):
    parser = HYConceptParser()
    result = []
    real_urls = []
    if len(failed_gn_main_url) != 0:
       real_urls = failed_gn_main_url
    else:
        for i in range(1, 6):
            real_url = (gn_main_url % i)
            real_urls.append(real_url)
    for real_url in real_urls:
        response = requests.get(real_url,headers=header_gn_main, verify=False)
        res = parser.parse_main(response.text)
        if len(res) == 0:
           print(real_url) 
        result += res   
        time.sleep(random.randint(10,15))
    print(result)    

def func(url, hygnList, failed=[]):
    exists_df = pd.read_sql('select * from ths_concept', con=engine)  
    parser = HYConceptParser()
    if len(failed) > 0:
       for item in failed:
           header['X-Requested-With'] = 'XMLHttpRequest'
           response = requests.get(item[0],headers=header, verify=False)   
           parsePage(parser, response.text, item[0], item[1], exists_df)
           time.sleep(random.randint(10,15))
       return    
    for first_real_url in hygnList:
        response = requests.get(first_real_url[0],headers=header, verify=False)
        g = re.match('(.+)(\d{6})/', first_real_url[0])
        code = g.group(2)
        total_page = parser.get_page_info(response.text)
        parsePage(parser, response.text, first_real_url[0], first_real_url[1], exists_df)
        time.sleep(random.randint(10,15))
        if total_page > 1:
           for i in range(2, total_page + 1):
               real_url = (url % i) + code+'/'
               header['X-Requested-With'] = 'XMLHttpRequest'
               response = requests.get(real_url,headers=header, verify=False)   
               parsePage(parser, response.text, real_url, first_real_url[1], exists_df)  
               time.sleep(random.randint(10,15))

# func(hyURL,hy)
# main_page()    
func(gnURL,gn)

