# -*-coding=utf-8-*-

__author__ = 'aqua'

import tushare as ts
import sys
sys.path.append('..')
from utils.Utils import Utils
from config.Config import Config
from sqlalchemy import create_engine

setting = Config()
engine = create_engine(setting.get_DBurl())


def cb(**kw):
    return ts.xsg_data()
Utils.queryData('xsg','code',engine, cb, forceUpdate=True)

def cb1(**kw):
    return ts.fund_holdings(2017, 4)
Utils.queryData('fund','code',engine, cb1, forceUpdate=True)