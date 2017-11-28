# -*-coding=utf-8-*-
__author__ = 'aqua'


import tushare as ts

print(ts.get_hist_data('000888')[-30:])