# -*-coding=utf-8-*-
__author__ = 'aqua'

from lxml import etree

class HYConceptParser():
      
    
      def get_page_info(self, html):
          page = etree.HTML(html)
          span = page.xpath('//span[@class="page_info"]')  
          if len(span) > 0:
             total = span[0].text
             return int(total.split('/')[1])
          return 0


      def parse_main(self, html):
          tuples = []
          page = etree.HTML(html)
          trs = page.xpath('//table[@class="m-table J-ajax-table"]/tbody/tr')
          i = 0
          while i < len(trs):
                name = trs[i].getchildren()[1].getchildren()[0].text
                link = trs[i].getchildren()[1].getchildren()[0].get('href')
                tuples.append((link, name))
                i = i + 1
          return tuples    

      def parse(self,html):
          codes = []
          page = etree.HTML(html)
      #     span = page.xpath('//div[@class="board-hq"]/h3/span')
      #     cont = span[0].text
          trs = page.xpath('//table[@class="m-table m-pager-table"]/tbody/tr')
          i = 0
          while i < len(trs):
                code = trs[i].getchildren()[1].getchildren()[0].text
                codes.append(code)
                i = i + 1
          return codes    
            #   name = tr.getchildren()[2].getchildren()[0].text
            #   print("insert into concept values('"+cont+"','"+code+"','"+name+"');") 

      