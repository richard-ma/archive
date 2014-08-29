from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from archive.items import ArchiveItem

from ConfigParser import ConfigParser

class ArchiveSpider(CrawlSpider):
    config = ConfigParser()
    name = 'archive'

    def __init__(self):
        self.config.read('./configrations.ini')
        self.allowed_domains = ['web.archive.org']
        self.start_urls = ['http://web.archive.org/web/20120114003207/http://mobilezonegt.com/']
        self.rules = (
            Rule(SgmlLinkExtractor(allow=(r'http://web\.archive\.org/.*/http://mobilezonegt\.com/')), callback='parse_item', follow=True),
            )

    def parse_item(self, response):
        item = ArchiveItem()

        item['url'] = response.url
        item['content'] = response.body

        return item
