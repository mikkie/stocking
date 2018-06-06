#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""使用urllib2请求代理服务器
请求http和https网页均适用
"""

import tushare
import threading
import time
from urllib.request import urlopen, Request
import base64
import zlib

#要访问的目标网页
page_url = "http://hq.sinajs.cn/rn=3860948606925&list=sh603999,sh603996,sh603988,sh603987,sh603978,sh603977,sh603976,sh603970,sh603969,sh603966,sh603963,sh603960,sh603959,sh603958,sh603955,sh603937,sh603936,sh603933,sh603929,sh603928,sh603922,sh603920,sh603917,sh603916,sh603912,sh603908,sh603906,sh603903,sh603897,sh603890,sh603888,sh603887,sh603886,sh603882,sh603881,sh603876,sh603861,sh603860,sh603859,sh603856,sh603848,sh603829,sh603826,sh603822,sh603819,sh603817,sh603813,sh603811,sh603809,sh603803,sh603800,sh603798,sh603797,sh603779,sh603778,sh603777,sh603776,sh603738,sh603733,sh603727,sh603725,sh603722,sh603721,sh603717,sh603716,sh603712,sh603711,sh603709,sh603707,sh603703,sh603701,sh603689,sh603688,sh603685,sh603683,sh603680,sh603677,sh603676,sh603668,sh603661,sh603656,sh603655,sh603648,sh603638,sh603637,sh603633,sh603630,sh603628,sh603626,sh603619,sh603618,sh603615,sh603612,sh603608,sh603607,sh603605,sh603603,sh603596,sh603577,sh603559,sh603557,sh603535,sh603533,sh603528,sh603527,sh603518,sh603516,sh603507,sh603506,sh603500,sh603499,sh603477,sh603466,sh603429,sh603421,sh603398,sh603396,sh603393,sh603388,sh603378,sh603367,sh603366,sh603365,sh603363,sh603359,sh603356,sh603339,sh603336,sh603330,sh603329,sh603323,sh603322,sh603321,sh603319,sh603309,sh603305,sh603299,sh603289,sh603283,sh603278,sh603277,sh603266,sh603258,sh603238,sh603232,sh603225,sh603218,sh603200,sh603189,sh603186,sh603183,sh603181,sh603179,sh603177,sh603168,sh603166,sh603165,sh603161,sh603157,sh603139,sh603138,sh603136,sh603133,sh603131,sh603129,sh603128,sh603126,sh603118,sh603110,sh603106,sh603103,sh603101"

#代理服务器
proxy = "47.101.38.210:16818"

#用户名和密码(私密代理/独享代理)
username = b"842958037"
password = b"7mqzliim"

def fun_timer():
    try:
       req = Request(page_url)
       req.add_header("Accept-Encoding", "Gzip") #使用gzip压缩传输数据让访问更快
       auth = base64.b64encode('842958037:7mqzliim'.encode('utf-8'))
       req.add_header("Proxy-Authorization", "Basic ODQyOTU4MDM3OjdtcXpsaWlt")
       req.set_proxy(proxy, "http")
       r = urlopen(req)

       content_encoding = r.headers["Content-Encoding"]
       if content_encoding and "gzip" in content_encoding:
          print(zlib.decompress(r.read(), 16+zlib.MAX_WBITS)) #获取页面内容
       else:
           print(r.read())  #获取页面内容
    except Exception as e:
           print("error")
           pass
    global timer
    timer = threading.Timer(3, fun_timer)
    timer.start()

timer = threading.Timer(3, fun_timer)
timer.start()        