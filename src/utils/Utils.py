# -*-coding=utf-8-*-
__author__ = 'aqua'

import numpy as np
import pandas as pd

class Utils(object):
      pass
      
      @staticmethod
      def trendline(data, order=1):
         coeffs = np.polyfit(data.index.values, list(data), order)
         slope = coeffs[-2]
         return float(slope)