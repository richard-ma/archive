from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from archive.items import PageItem

class PageSpider(CrawlSpider):
    name = "page"
    allowed_domains = ["web.archive.org"]
    #allowed_domains = ["mobilezonegt.com"]
    start_urls = [
            "http://web.archive.org/web/20120114003207/http://mobilezonegt.com/",
            #"http://mobilezonegt.com/"
            ]

    rules = (
            #Rule(SgmlLinkExtractor(allow=(r'.*')),
                #callback='parse_item',
                #follow=True),
            Rule(SgmlLinkExtractor(allow=(r'.*/http://mobilezonegt\.com/.*')),
                callback='parse_item',
                follow=True),
            )

    def parse_item(self, response):
        #hxs = HtmlXPathSelector(response)
        item = PageItem()
        item['url'] = response.url
        item['content'] = response.body
        return item
