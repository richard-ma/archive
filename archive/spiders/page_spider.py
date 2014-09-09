from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from archive.items import PageItem

import os
import re
from ConfigParser import ConfigParser

class PageSpider(CrawlSpider):
    config = ConfigParser()

    name = "page"

    def __init__(self):

        # init spider
        self.config.read('./configrations.ini')

        self.allowed_domains = ["web.archive.org"]
        self.start_urls = [
            self.config.get('target', 'startUrl'),
            ]
        self.rules = (
            Rule(SgmlLinkExtractor(
                    allow=(r'.*/http://%s/.*' % self.config.get('target', 'domain').replace('.', '\.')),
                    deny_extensions='', # http://www.haogongju.net/art/1690534
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

        config = _get_config()
        data_path = config.get('storage', 'path')

        url = _get_real_path(item['url'])
        # can not find real path of a link
        if url == None:
            return item

        path_array = url.split('/')

        full_filename = ''
        if '?' in path_array[-1]: # have params
            # replace ?=& to -
            url = url.replace('?', '-')
            url = url.replace('=', '-')
            url = url.replace('&', '-')

            full_filename = data_path + url
        else:
            if '.' in path_array[-1]: # filename
              full_filename = data_path + url
            else: # static url
                if url[-1] != '/': # not have tail '/'
                    url = url + '/' # add tail '/'
                full_filename = data_path + url + 'index.html' # /index.html

        dir_path = os.path.dirname(full_filename)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        fd = open(full_filename, 'a')
        content = _replace_url(str(item['content']))
        fd.write(content)
        fd.close()

        return item

def _get_config():
    config = ConfigParser()
    config.read('./configrations.ini')
    return config

def _get_real_path(path):
    config = _get_config()
    r = r"http://web\.archive\.org/.*/http://%s(.*)" % _regular_expression_escape(config.get('target', 'domain'))
    real_path = re.findall(r, path)
    if real_path.count() < 1:
        return None
    else:
        return real_path[0]

def _regular_expression_escape(s):
    return s.replace('.', '\.')

def _replace_url(content):
    config = _get_config()
    links = re.findall(r'/web/[0123456789imcs_\*]*/[^\'\"]*', content)
    for link in links:
        newLink = _new_link(link)
        #log.msg('!!!!NewLink: %s' % re.escape(newLink))
        re.sub(re.escape(link), newLink, content)
    content = re.sub(r'/web/[0123456789imcs_\*]*/', '', content)
    return content

def _new_link(url):
    # split url into array through '/'
    path_array = url.split('/')

    if '?' in path_array[-1]: # have params
        # replace ?=& to -
        url = url.replace('?', '-')
        url = url.replace('=', '-')
        url = url.replace('&', '-')
    else:
        if '.' in path_array[-1]: # filename
            pass
        else: # static url
            if url[-1] != '/': # not have tail '/'
                url = url + '/' # add tail '/'
            url = url + 'index.html' # /index.html

    return url
