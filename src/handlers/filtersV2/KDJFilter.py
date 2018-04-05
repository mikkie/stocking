# -*-coding=utf-8-*-
__author__ = 'aqua'

import numpy as np
import sys
sys.path.append('..')
from utils.Utils import Utils

class KDJFilter(object):
    pass

    def filter(self, data, config):
        return self.isKdjKingCross(data, data['df_3m'])

    def isKdjKingCross(self, data, df_3m):
        yesterdayK = df_3m.iloc[-1].get('k')
        yesterdayD = df_3m.iloc[-1].get('d')
        yesterdayJ = df_3m.iloc[-1].get('j')
        lastK = df_3m.iloc[-2].get('k')
        lastD = df_3m.iloc[-2].get('d')
        lastJ = df_3m.iloc[-2].get('j')
        tdbfyK = df_3m.iloc[-3].get('k')
        tdbfyD = df_3m.iloc[-3].get('d')
        tdbfyJ = df_3m.iloc[-3].get('j')
        data['kdj'] = 0
        flag = lastK < 20 and lastD < 20 and lastJ < 20 and tdbfyD > tdbfyK and lastD <= lastK and yesterdayD <= yesterdayK
        if flag:
           data['kdj'] = 1 
        return flag 