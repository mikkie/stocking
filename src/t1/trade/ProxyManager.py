# -*-coding=utf-8-*-
__author__ = 'aqua'
from concurrent.futures import ThreadPoolExecutor,as_completed
import sys
import threading
from ..MyLog import MyLog
sys.path.append('..')
import src.config.Config
import base64
import tushare
import requests
import json

class ProxyManager(object):
     
      PROXY_URL = 'http://webapi.http.zhimacangku.com/getip?num={proxy_size}&type=2&pro=0&city=0&yys=100017&port=11&time=4&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=1&regions=310000,320000,330000,350000,440000'

      def __init__(self, proxy_size):
          self.a_list = []
          self.proxy_size = proxy_size
          self.proxy_url = ProxyManager.PROXY_URL.format(proxy_size=proxy_size)
          self.threadLock = threading.Lock()
          self.a_list.append(
              {"ip":"local","port":0}
          )
          self.b_list = []
          self.current_list = self.a_list
          self.config = src.config.Config.Config()
          self.executor = ThreadPoolExecutor(max_workers=15)
          self.load_proxy()

      def load_proxy(self):
          proxy_list = []
          try:
              response = requests.get(self.proxy_url)
              result = json.loads(response.text)
              proxy_list = result['data']
          except Exception as e:
                 pass    
          if len(proxy_list) == self.proxy_size:
             for proxy in proxy_list: 
                 self.current_list.append(proxy)
          else:
              MyLog.error('can not get proxy')

      def get_proxy(self):
          self.threadLock.acquire()
          if len(self.current_list) == 0:
             self.threadLock.release()
             return None
          proxy = self.current_list.pop(0)
          self.threadLock.release()
          return proxy


      def return_proxy(self,proxy):
          self.current_list.append(proxy) 


      def get_proxy_size(self):
          return len(self.current_list)       


      def add_proxy(self,req):
          proxy = self.get_proxy()
          if proxy is not None and proxy['ip'] != 'local':
             if 'username' in proxy and proxy['username'] != '' and 'password' in proxy and proxy['password'] != '': 
                auth = base64.b64encode((proxy['username'] + ':' + proxy['password']).encode('utf-8'))
                req.add_header("Proxy-Authorization", "Basic " + auth.decode('utf-8')) 
             req.set_proxy(proxy['ip'] + ':' + str(proxy['port']), "http")
          return proxy  


      def retry_wrapper(self,codeList,proxyManager=None):
          try:
             return tushare.get_realtime_quotes(codeList,proxyManager=proxyManager) 
          except Exception as e:
                 print(e)
                #  return tushare.get_realtime_quotes(codeList,proxyManager=self)   
                    
             


      def thread_task(self,code_split_list,*args,async_exe=None):
          #force proxy for batch
          df = self.retry_wrapper(code_split_list,proxyManager=self)
          if df is not None:
             if async_exe is not None:
                async_exe(df,*args)
             else:
                 return df      

      #force proxy for multithread batch request, option proxy or not for no batch 
      def get_realtime_quotes(self,code_list,*args,batch_size=0,async_exe=None,use_proxy_no_batch=False):
          if batch_size == 0:
             res_df = None
             #force proxy for no batch
             if use_proxy_no_batch:
                res_df = self.retry_wrapper(code_list,proxyManager=self) 
             else:   
                 res_df = self.retry_wrapper(code_list)
             if async_exe is not None:
                async_exe(res_df,*args)
                return None
             else:
                 return res_df    
          total = len(code_list)
          thread_size = total // batch_size
          less = total % batch_size
          if less > 0:
             thread_size = thread_size + 1 
          start = 0
          end = batch_size
          features = []
          for i in range(thread_size):
              code_split_list = code_list[start:end]
              if async_exe is not None:
                 self.executor.submit(self.thread_task,code_split_list,*args,async_exe=async_exe)
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



              
                           
          
                       

