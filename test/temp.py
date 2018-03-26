# -*-coding=utf-8-*-
__author__ = 'aqua'

import datetime as dt

now = dt.datetime.now()
last_time = dt.datetime.strptime('2018-03-26' + ' ' + '10:21:10', '%Y-%m-%d %H:%M:%S')
print((now - last_time).seconds)