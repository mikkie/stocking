# -*-coding=utf-8-*-
__author__ = 'aqua'
import sys
sys.path.append('..')
import src.config.Config
import base64

class ProxyManager(object):

      def __init__(self):
          self.a_list = []
          self.a_list.append(
              {
                'host' : 'local',
                'username' : '',
                'password' : ''
              }
          )
          self.b_list = []
          self.current_list = self.a_list
          self.config = src.config.Config.Config()
          self.load_proxy()

      def load_proxy(self):
          proxy_list = self.config.get_t1()['proxy']
          if len(proxy_list) > 0:
             for proxy in proxy_list: 
                 self.current_list.append(proxy)

      def get_proxy(self):
          if len(self.current_list) == 0:
             if self.current_list == self.a_list:
                self.current_list = self.b_list
             else:
                 self.current_list = self.a_list
          if self.current_list == 0:
             return None
          proxy = self.current_list.pop(0)
          self.current_list.append(proxy)
          return proxy    


      def move_to_backup(self):
          backup_list = None
          if self.current_list == self.a_list:
             backup_list = self.b_list
          else:
               backup_list = self.a_list 
          proxy = self.current_list.pop(-1)     
          backup_list.append(proxy)  


      def add_proxy(self,req):
          proxy = self.get_proxy()
          if proxy is not None and proxy['host'] != 'local':
             if proxy['username'] != '' and proxy['password'] != '': 
                auth = base64.b64encode((proxy['username'] + ':' + proxy['password']).encode('utf-8'))
                req.add_header("Proxy-Authorization", "Basic " + auth.decode('utf-8')) 
             req.set_proxy(proxy['host'], "http")
          return proxy   
              
                           
          
                       

