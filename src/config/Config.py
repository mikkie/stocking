# -*-coding=utf-8-*-
__author__ = 'aqua'

class Config(object):

      def __init__(self):
          self.__pKm5Change = 0.03 #振幅
          self.__superSold = 0.2 #超卖
          self.__dbUrl = 'mysql://root:aqua@10.172.97.136/stocking?charset=utf8' #数据库地址

      def get_pKm5Change(self):
          return self.__pKm5Change

      def get_SuperSold(self):
          return self.__superSold  

      def get_DBurl(self):
          return self.__dbUrl  

      pass