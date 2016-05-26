from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class JsonWithEncodingCnblogsPipeline(object):
    def __init__(self):
        self.file = codecs.open('cnblogs3.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'  
        #print line
        self.file.write(line.decode("unicode_escape"))  
        return item 
    def spider_closed(self, spider):
        self.file.close()

class MySQLStoreCnblogsPipeline(object):
    def __init__(self, dbpool):
        #print "i was th2"
        self.dbpool = dbpool
    
    @classmethod
    def from_settings(cls, settings):
        #print "i was there2"
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    #pipeline
    def process_item(self, item, spider):
        #print "i was thdd"
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _do_upinsert(self, conn, item, spider):
        #print "i was th2sdsd"
        linkmd5id = self._get_linkmd5id(item)
        #print linkmd5id
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from t_talents where linkmd5id = %s
        """, (linkmd5id, ))
        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update t_talents set identify=%s, title = %s, name = %s, phone = %s,email = %s, location = %s, 
                imgurl=%s, srclink = %s, profile=%s, updated = %s where linkmd5id = %s
            """, (item['identify'], item['title'], item['name'], item['phone'], item['email'], item['location'],item['imgurl'], item['srclink'],item['profile'], now, linkmd5id))
            # print """
            #      update t_talents set identify=%s, title = %s, name = %s, phone = %s,email = %s, location = %s, 
            #     imgurl=%s, srclink = %s, profile=%s, updated = %s where linkmd5id = %s
            # """, (item['identify'], item['title'], item['name'], item['phone'], item['email'], item['location'],item['imgurl'], item['srclink'],item['profile'], now, linkmd5id)
        else:
            conn.execute("""
                insert into t_talents(linkmd5id, identify, title, name, phone, email,
                    location, imgurl, srclink, profile, updated) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
            """, (linkmd5id, item['identify'], item['title'], item['name'], item['phone'], item['email'],item['location'], item['imgurl'], item['srclink'], item['profile'], now))
            # print """
            #     insert into t_talents(linkmd5id, identify, title, name, phone, email,
            #         location, imgurl, srclink, profile, updated) 
            #     values(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            # """, (linkmd5id, item['identify'], item['title'], item['name'], item['phone'], item['email'],item['location'], item['imgurl'], item['srclink'], item['profile'], now)

    def _get_linkmd5id(self, item):
        return md5(item['identify']).hexdigest()

    def _handle_error(self, failue, item, spider):
        log.err(failure)