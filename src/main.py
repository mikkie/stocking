# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd
import handlers.dadStrategy as ds
import config.Config as conf
from sqlalchemy import create_engine


def getData():
    engine = create_engine('mysql://root:aqua@10.172.97.136/stocking?charset=utf8')
    df_hist_5 = pd.read_sql_table('km5', con=engine)
    return df_hist_5

setting = conf.Config()
dad = ds.DadStrategy()
data = getData()
dad.chooseStock(data,setting)

