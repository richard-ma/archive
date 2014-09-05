# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os
import re
from ConfigParser import ConfigParser

class PagePipeline(object):
    def process_item(self, item, spider):
        data_path = './data'

        url = _get_real_path(item['url'])[0]

        full_filename = data_path + url
        if os.path.isdir(full_filename):
            full_filename = full_filename + 'index.html'

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
    return real_path

def _regular_expression_escape(s):
    return s.replace('.', '\.')

def _replace_url(content):
    config = _get_config()
    return re.sub(r'/web/[0123456789imcs_\*]*/', '', content)
