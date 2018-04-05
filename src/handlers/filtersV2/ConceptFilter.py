# -*-coding=utf-8-*-
__author__ = 'aqua'

class ConceptFilter(object):
      pass

      def filter(self, data, config):
          conceptList = config.get_conceptCodes()
          if len(conceptList) == 0:
             data['concept'] = 1
             return True 
          if data['code'] in conceptList:
             data['concept'] = 1 
             return True
          data['concept'] = 0  
          return False   