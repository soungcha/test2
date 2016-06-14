from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5


class JsonWithEncodingMythridPipeline(object):
    def __init__(self):
        self.file = codecs.open('mythird.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'  
        #print line
        self.file.write(line.decode("unicode_escape"))  
        return item 
    def spider_closed(self, spider):
        self.file.close()# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

