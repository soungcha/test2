# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    imgurl = scrapy.Field()
    profile = scrapy.Field()
    srclink = scrapy.Field()
