# -*-coding=utf-8-*-
__author__ = 'aqua'

import os
import re
from sqlalchemy import create_engine
import requests

URL = 'http://stock.stcn.com/2018/1017/14586879.shtml'
load_dir = '../../data/temp1'
engine = create_engine('mysql://pig:pigpiggo@112.124.69.222/stocking?charset=utf8')
path = os.path.join(os.path.dirname(__file__), load_dir)
for file in os.listdir(path):
    codes = []
    try:
        htmlf = open(path + '/' + file,'r',encoding="utf-8")
        htmlcont= htmlf.read()
        codes = re.findall('\d{6}',htmlcont)
        with engine.connect() as conn:
             sql = 'update today_all set pick = 1 where code in %s' % str(tuple(codes))
             conn.execute(sql)
    except Exception as e:
           print('failed to read %s, e=%s' % (file,e))
