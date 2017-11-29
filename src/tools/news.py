# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import sys
sys.path.append('..')
from config.Config import Config
from sqlalchemy import create_engine

setting = Config()
engine = create_engine(setting.get_DBurl())
df_news = ts.get_latest_news(top=10,show_content=True)
df_news.to_sql('news',con=engine,if_exists='replace')

df_news_highlight = ts.guba_sina(show_content=True)
df_news_highlight.to_sql('news_highlight',con=engine,if_exists='replace')