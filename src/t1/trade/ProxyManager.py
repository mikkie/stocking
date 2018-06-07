# -*-coding=utf-8-*-
__author__ = 'aqua'
import sys
sys.path.append('..')
from queue import Queue
import config.Config

class ProxyManager(object):

      def __init__(self):
          self.a_queue = Queue()
          self.a_queue.put(
              {
                  'host' : 'local',
                  'username' : '',
                  'password' : ''
              }
          )
          self.b_queue = Queue()
          self.current_queue = self.a_queue
          self.config = config.Config.Config()
          self.load_proxy()

      def load_proxy(self):
          proxy_list = self.config.get_t1()['proxy']
          if len(proxy_list) > 0:
             for proxy in proxy_list: 
                 self.current_queue.put(proxy)

      def get_proxy(self):
          if self.current_queue.empty():
             if self.current_queue == self.a_queue:
                self.current_queue = self.b_queue
             else:
                 self.current_queue = self.a_queue
          if self.current_queue.empty():
             return None
          proxy = self.current_queue.get()
          self.current_queue.put(proxy)
          return proxy    


      def add_proxy(self):
          proxy = self.get_proxy()
          if proxy is not None:
              
                           
          
                       

