# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import math
import threading
import time
import pandas as pd
from datetime import datetime


def calculate():
    timer = threading.Timer(2, calculate)
    timer.start()

timer = threading.Timer(2, calculate)
timer.start()

while True:
      time.sleep(0.01)
pass