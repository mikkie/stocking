# -*-coding=utf-8-*-
__author__ = 'aqua'

import logging

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler("../log/stocking.log", "w",encoding = "UTF-8")
consoleHandler = logging.StreamHandler()
root_logger.addHandler(fileHandler)
root_logger.addHandler(consoleHandler)

class MyLog(object):
    
      @staticmethod
      def info(msg):
          logging.info(msg) 

      @staticmethod
      def error(msg):
          logging.error(msg)



