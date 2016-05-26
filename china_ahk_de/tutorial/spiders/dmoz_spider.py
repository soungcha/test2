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
        "http://china.ahk.de/cn/about-us/contact-us-in/north-china/",
        "http://china.ahk.de/cn/about-us/contact-us-in/east-china/",
        "http://china.ahk.de/cn/about-us/contact-us-in/south-southwest-china/",
        "http://china.ahk.de/cn/about-us/contact-us-in/hong-kong/",
        "http://china.ahk.de/cn/about-us/contact-us-in/taiwan/",
        "http://china.ahk.de/cn/about-us/contact-us-in/germany/"

    ]

    def parse(self, response):
        sel = Selector(response)
        #sites = sel.xpath('//div[@id="navsecond"]/div[@id="course"]/ul[1]/li')
        sites = sel.css(".cp-list__item")
        location = sel.css("h1.grey_underline").xpath("text()").extract()
        thelocation = location[0].encode('utf-8') if len(location)>0 else ""
        items = []  
        i = 0  
        for site in sites:
            if i<3:  
                item = DmozItem()  
                
                name = site.css("p.cp-list__item-name").xpath("./span[@itemprop='name']/text()").extract()
                title = site.css("p.cp-list__item-function").xpath("text()").extract()
                phone = site.css("span.phone").xpath("text()").extract()
                imgurl = site.css("img").xpath("@src").extract()
                


                item['name'] = name[0].encode('utf-8') if len(name)>0 else ""
                item['title'] = title[0].encode('utf-8') if len(title)>0 else "" 
                item['phone'] = phone[0].encode('utf-8') if len(phone)>0 else ""
                item['imgurl'] = "http://china.ahk.de/"+ imgurl[0].encode('utf-8') if len(imgurl)>0 else ""
                item['email'] = ""
                item['srclink'] = "http://china.ahk.de/cn/about-us/contact-us-in/north-china/"
                item["identify"] = item['phone'] + item['name']
                item["profile"] = ""
                item['location'] = thelocation

                items.append(item) 
                #log.msg("Appending item...",level='INFO')  
  
  
        #log.msg("Append done.",level='INFO')  
        return items 