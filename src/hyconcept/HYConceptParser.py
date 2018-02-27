# -*-coding=utf-8-*-
__author__ = 'aqua'

from lxml import etree

class HYConceptParser():
      pass

      def parse(self,html):
          page = etree.HTML(html)
          span = page.xpath('//div[@class="board-hq"]/h3/span')
          cont = span.text
          trs = page.xpath('//table[@class="m-table m-pager-table"]/tbody/tr')
          for tr in trs:
              code = tr.getchildren()[1].getchildren()[0].text
              name = tr.getchildren()[2].getchildren()[0].text
              print("insert into concept values('"+cont+"','"+code+"','"+name+"');") 

      