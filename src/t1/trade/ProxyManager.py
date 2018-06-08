# -*-coding=utf-8-*-
__author__ = 'aqua'
from concurrent.futures import ThreadPoolExecutor,as_completed
import sys
sys.path.append('..')
import src.config.Config
import base64
import tushare

class ProxyManager(object):

      def __init__(self):
          self.a_list = []
          self.a_list.append(
              {
                      'host' : '117.27.26.114:4275',
                      'username' : '',
                      'password' : ''
              }
          )
          self.b_list = []
          self.current_list = self.a_list
          self.config = src.config.Config.Config()
          self.executor = ThreadPoolExecutor(max_workers=15)
          self.load_proxy()

      def load_proxy(self):
          proxy_list = self.config.get_t1()['proxy']
          if len(proxy_list) > 0:
             for proxy in proxy_list: 
                 self.current_list.append(proxy)

      def get_proxy(self):
          proxy = self.current_list.pop(0)
          self.current_list.append(proxy)
          return proxy    


      def add_proxy(self,req):
          proxy = self.get_proxy()
          if proxy is not None and proxy['host'] != 'local':
             if proxy['username'] != '' and proxy['password'] != '': 
                auth = base64.b64encode((proxy['username'] + ':' + proxy['password']).encode('utf-8'))
                req.add_header("Proxy-Authorization", "Basic " + auth.decode('utf-8')) 
             req.set_proxy(proxy['host'], "http")
          return proxy   


      def thread_task(self,code_split_list,async_exe=None):
          df = tushare.get_realtime_quotes(code_split_list,add_proxy=self.add_proxy)
          if df is not None:
             if async_exe is not None:
                async_exe(df)
             else:
                 return df      


      def get_realtime_quotes(self,code_list,batch_size=0,async_exe=None):
          if batch_size == 0:
             return tushare.get_realtime_quotes(code_list)
          total = len(code_list)
          thread_size = total // batch_size + 1 
          start = 0
          end = batch_size
          features = []
          for i in range(thread_size):
              code_split_list = code_list[start:end]
              if async_exe is not None:
                 self.executor.submit(self.thread_task,code_split_list,async_exe=async_exe)
              else:
                  future = self.executor.submit(self.thread_task,code_split_list) 
                  features.append(future)
              start = end
              end = start + batch_size
              if end > total:
                 end = total
          if async_exe is None:
             result_df = None 
             for feature in as_completed(features):
                 if result_df is None:
                    result_df = feature.result() 
                 else:
                     result_df = result_df.append(feature.result(),ignore_index=True)   
             return result_df              



              
                           
          
                       

