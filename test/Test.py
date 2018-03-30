# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd
import tushare as ts

df = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
print(df)