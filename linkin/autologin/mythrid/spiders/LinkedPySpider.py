import argparse,os,time
import urlparse,random
from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule

from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector

from mythrid.items import LinkedPyItem

class LinkedPySpider(InitSpider):
    name = 'LinkedPy'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = ["http://www.linkedin.com/csearch/results?type=companies&keywords=&pplSearchOrigin=GLHD&pageKey=member-home&search=Search#facets=pplSearchOrigin%3DFCTD%26keywords%3D%26search%3DSubmit%26facet_CS%3DC%26facet_I%3D80%26openFacets%3DJO%252CN%252CCS%252CNFR%252CF%252CCCR%252CI"]

    def init_request(self):
        time.sleep(random.uniform(15.6,20.9))
        #"""This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        #"""Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'session_key': 'soungcha2005@hotmail.com', 'session_password': 'Ysdss2016'},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        #"""Check the response returned by a login request to see if we aresuccessfully logged in."""
        if "Sign Out" in response.body:
            self.log("\n\n\nSuccessfully logged in. Let's start crawling!\n\n\n")
            # Now the crawling can begin..

            return self.initialized() # ****THIS LINE FIXED THE LAST PROBLEM*****

        else:
            self.log("\n\n\nFailed, Bad times :(\n\n\n")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse(self, response):
        time.sleep(random.uniform(10.6,20.9))
        self.log("\n\n\n We got data! \n\n\n")
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ol[@id=\'result-set\']/li')
        items = []
        for site in sites:
            item = LinkedPyItem()
            item['title'] = site.select('h2/a/text()').extract()
            item['link'] = site.select('h2/a/@href').extract()
            items.append(item)
        return items