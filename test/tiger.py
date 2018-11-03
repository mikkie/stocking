# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts

df = ts.get_realtime_quotes(['300698'])
print(df)