#coding:utf-8
import scrapy
from scrapy.selector import Selector
#from scrapy import log

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "w3school"
    allowed_domains = ["w3school.com.cn"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        "http://www.w3school.com.cn/xml/xml_syntax.asp" 
    ]

    def parse(self, response):
        sel = Selector(response)  
        sites = sel.xpath('//div[@id="navsecond"]/div[@id="course"]/ul[1]/li')  
        items = []  
  
        for site in sites:  
            item = DmozItem()  
  
            title = site.xpath('a/text()').extract()  
            link = site.xpath('a/@href').extract()  
            desc = site.xpath('a/@title').extract()  
  
            item['title'] = [t.encode('utf-8') for t in title]  
            item['link'] = [l.encode('utf-8') for l in link]  
            item['desc'] = [d.encode('utf-8') for d in desc]  
            items.append(item)  
  
            #记录  
            #log.msg("Appending item...",level='INFO')  
  
  
        #log.msg("Append done.",level='INFO')  
        return items 