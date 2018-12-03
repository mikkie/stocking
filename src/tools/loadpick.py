# -*-coding=utf-8-*-
__author__ = 'aqua'

import os
import re
from lxml import etree
from sqlalchemy import create_engine


load_dir = '../../data/temp'
engine = create_engine('mysql://pig:pigpiggo@112.124.69.222/stocking?charset=utf8')
path = os.path.join(os.path.dirname(__file__), load_dir)
for file in os.listdir(path):
    codes = []
    try:
        htmlf = open(path + '/' + file,'r',encoding="utf-8")
        htmlcont= htmlf.read()
        page = etree.HTML(htmlcont)
        trs = page.xpath('//table/tr')
        i = 0
        while i < len(trs):
              code = trs[i].getchildren()[0].text.strip()
              if re.match('^\d{6}.(SH|SZ)$',code) is not None:
                 code = code.replace('.SH','').replace('.SZ','')
                 codes.append(code)
              i += 1    
        with engine.connect() as conn:
             sql = 'update today_all set pick = 1 where code in %s' % str(tuple(codes))
             conn.execute(sql)
    except Exception as e:
           print('failed to read %s, e=%s' % (file,e))    
