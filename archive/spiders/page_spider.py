from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from archive.items import PageItem

from ConfigParser import ConfigParser

class PageSpider(CrawlSpider):
    config = ConfigParser()
    name = 'page'
    allowed_domains = ["web.archive.org"]

    start_urls = [
            "http://web.archive.org/web/20120114003207/http://mobilezonegt.com/",
            ]

    rules = (
            Rule(SgmlLinkExtractor(allow=(r'.*/http://mobilezonegt\.com/.*')),
                callback='parse_item',
                follow=True),
            )

    def __init__(self):
        self.config.read('./configrations.ini')
        #self.allowed_domains = ['web.archive.org']
        #self.start_urls = ['http://web.archive.org/web/20120114003207/http://mobilezonegt.com/']
        #self.rules = [
            #Rule(SgmlLinkExtractor(allow=(r'.*/http://mobilezonegt\.com/.*')), callback='parse_item', follow=True),
            #]

    def parse_item(self, response):
        item = PageItem()

        item['url'] = response.url
        item['content'] = response.body

        return item
