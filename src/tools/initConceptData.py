# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
from lxml import etree

conceptHomeUrl = 'http://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/ajax/'
conceptUrl = 'http://q.10jqka.com.cn/gn/detail/order/desc/page/${pageNum}/ajax/1/code/${code}'
headersHomePage = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'uaid=3e9d33c7f0daebe595757fcd5d3722ba; spversion=20130314; searchGuide=sg; historystock=002046%7C*%7C603698%7C*%7C000901%7C*%7C300563%7C*%7C300565; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; __utma=156575163.844587348.1519633850.1525760999.1525775393.61; __utmc=156575163; __utmz=156575163.1525775393.61.61.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1525761708,1525767793,1525769729,1525775403; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1525394879,1525653828,1525740567,1525775403; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1525761708,1525767793,1525769729,1525775403; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1525779105; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1525779105; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1525779105; v=ApIkkJjeHNxyxGCgBrmEGuOd41Nwo5Q3yKKKd1zqvCcxkzxFRDPmTZg32nkv',
    'hexin-v': 'Au1bYes3S72bKy_RH-Lzm-AU_IJjSiTGq2-F5C_bK6zx8wN095ox7DvOlcy8',
    'Host': 'data.10jqka.com.cn',
    'Referer': 'http://data.10jqka.com.cn/funds/gnzjl/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

headersAjaxConcept = {
    'Accept': 'text/html, */*; q=0.01',
    'hexin-v': 'Au1bYes3S72bKy_RH-Lzm-AU_IJjSiTGq2-F5C_bK6zx8wN095ox7DvOlcy8',
    'Referer': 'http://q.10jqka.com.cn/gn/detail/code/301602/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
linksUrl = []

def parseHomePage(response):
    page = etree.HTML(response) 
    trs = page.xpath('//table[@class="m-table J-ajax-table"]/tbody/tr')
    for tr in trs:
        link = tr.getchildren()[1].getchildren()[0]
        linksUrl.append({'url' : link.get('href'),'cont' : link.text})

for i in range(1,5):
    response = requests.get(conceptHomeUrl + str(i)+'/',headers=headersHomePage, verify=False)
    parseHomePage(response.text)


def parsePage(response):
    page = etree.HTML(response) 
    span = page.xpath('//div[@class="board-hq"]/h3/span')
    code = span[0].text 
    return code


def parseAjaxPage(cont,response):
    page = etree.HTML(response) 
    span = page.xpath('//span[@class="page_info"]')
    totalPage = 1
    if len(span) > 0:
       totalPage = int(span[0].text.split('/')[1])
    trs = page.xpath('//table[@class="m-table m-pager-table"]/tbody/tr')
    for tr in trs:
        code = tr.getchildren()[1][0].text
        name = tr.getchildren()[2][0].text
        print("insert into concept values('"+cont+"','"+code+"','"+name+"');")
    return totalPage    

for link in linksUrl:
    data = link['url'].split('/')
    contCode = data[len(data) - 2]
    start = 1
    totalPage = 1
    while start <= totalPage:
          url = conceptUrl.replace('${pageNum}',str(start)).replace('${code}',contCode)
          response = requests.get(url,headers=headersAjaxConcept, verify=False)
          totalPage = parseAjaxPage(link['cont'],response.text)
          start = start + 1

    

