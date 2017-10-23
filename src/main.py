# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd
import handlers.dadStrategy as ds
import config.Config as conf
from sqlalchemy import create_engine


def getData(setting):
    engine = create_engine(setting.get_DBurl())
    df_hist_5 = pd.read_sql_table('km5', con=engine)
    return df_hist_5

setting = conf.Config()
dad = ds.DadStrategy()
data = getData(setting)
dad.chooseStock(data,setting)

