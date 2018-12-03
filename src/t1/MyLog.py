# -*-coding=utf-8-*-
__author__ = 'aqua'

import logging
import datetime as dt
import os

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler("../log/stocking" + str(os.getpid()) + ".log", "w",encoding = "UTF-8")
consoleHandler = logging.StreamHandler()
root_logger.addHandler(fileHandler)
root_logger.addHandler(consoleHandler)
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.ERROR)  

class MyLog(object):
    
      @staticmethod
      def info(msg):
          logging.info('[%s] %s' % (dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg))

      @staticmethod
      def error(msg):
          logging.error('[%s] %s' % (dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg))

      @staticmethod
      def warn(msg):
          logging.warn('[%s] %s' % (dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg))

      @staticmethod
      def debug(msg):
          logging.debug('[%s] %s' % (dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg))        



