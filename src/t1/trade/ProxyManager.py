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
              {"ip":"222.219.154.84","port":4236}
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
          if len(self.current_list) == 0:
             return None
          proxy = self.current_list.pop(0)
          return proxy


      def return_proxy(self,proxy):
          self.current_list.append(proxy)    


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
                 return tushare.get_realtime_quotes(codeList,proxyManager=self)   
                    
             


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



              
                           
          
                       

