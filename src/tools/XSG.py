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

# def cb(**kw):
#     return ts.get_today_all()
# Utils.queryData('today_all','code',engine, cb, forceUpdate=True)

# def cb1(**kw):
#     return ts.xsg_data()
# Utils.queryData('xsg','code',engine, cb1, forceUpdate=True)

def cb2(**kw):
    return ts.fund_holdings(2017, 4)
Utils.queryData('fund','code',engine, cb2, forceUpdate=True)

# def cb3(**kw):
#     return ts.inst_tops(days=10)
# Utils.queryData('inst_tops','code',engine, cb3, forceUpdate=True)

# def cb4(**kw):
#     return ts.inst_detail()
# Utils.queryData('inst_detail','code',engine, cb4, forceUpdate=True)

# def cb5(**kw):
#     return ts.cap_tops(days=30)
# Utils.queryData('cap_tops','code',engine, cb5, forceUpdate=True)
