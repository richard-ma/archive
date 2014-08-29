from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from archive.items import PageItem

from ConfigParser import ConfigParser

class PageSpider(CrawlSpider):
    config = ConfigParser()

    name = "page"

    def __init__(self):

        # init spider
        self.config.read('./configrations.ini')

        self.allowed_domains = ["web.archive.org"]
        self.start_urls = [
            "http://web.archive.org/web/20120114003207/http://%s/" % self.config.get('target', 'domain'),
            ]
        self.rules = (
            Rule(SgmlLinkExtractor(
                    allow=(r'.*/http://%s/.*' % self.config.get('target', 'domain').replace('.', '\.')),
                    deny_extensions='',
                    tags=('a', 'area', 'link', 'script', 'img'),
                    attrs=('href', 'src'),
                    ),
                callback='parse_item',
                follow=True,
                ),
            )

        # call Crawlspider.__init__ to init a real spider
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        item = PageItem()
        item['url'] = response.url
        item['content'] = response.body
        return item
