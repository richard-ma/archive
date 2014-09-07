# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os
import re
from ConfigParser import ConfigParser

class PagePipeline(object):
    def process_item(self, item, spider):
        config = _get_config()
        data_path = config.get('storage', 'path')

        url = _get_real_path(item['url'])

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
    return real_path[0]

def _regular_expression_escape(s):
    return s.replace('.', '\.')

def _replace_url(content):
    config = _get_config()
    return re.sub(r'/web/[0123456789imcs_\*]*/', '', content)
