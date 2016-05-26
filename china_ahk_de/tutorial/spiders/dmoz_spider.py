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
        "http://china.ahk.de/cn/about-us/contact-us-in/north-china/" 
    ]

    def parse(self, response):
        sel = Selector(response)
        #sites = sel.xpath('//div[@id="navsecond"]/div[@id="course"]/ul[1]/li')
        sites = sel.css(".cp-list__item")
        items = []  
  
        for site in sites:  
            item = DmozItem()  
  
            name = site.css("p.cp-list__item-name").xpath("./span[@itemprop='name']/text()").extract()
            title = site.css("p.cp-list__item-function").xpath("text()").extract()
            phone = site.css("span.phone").xpath("text()").extract()
            imgurl = site.css("img").xpath("@src").extract()

            item['name'] = [n.encode('utf-8') for n in name] 
            item['title'] = [t.encode('utf-8') for t in title]  
            item['phone'] = [p.encode('utf-8') for p in phone] 
            item['imgurl'] = [l.encode('utf-8') for l in imgurl]
            item['email'] = ""
            item['srclink'] = "http://china.ahk.de/cn/about-us/contact-us-in/north-china/"

            items.append(item)  
  
            #记录  
            #log.msg("Appending item...",level='INFO')  
  
  
        #log.msg("Append done.",level='INFO')  
        return items 