# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os
import re

class PagePipeline(object):
    def process_item(self, item, spider):
        data_path = './data'

        url = _get_real_path(item['url'])[0]

        full_filename = data_path + url
        if os.path.isdir(full_filename):
            full_filename = full_filename + 'index.html'

        dir_path = os.path.dirname(full_filename)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        fd = open(full_filename, 'a')
        content = str(item['content'])
        fd.write(content)
        fd.close()

        return item

def _get_real_path(path):
    real_path = re.findall(r"http://web\.archive\.org/.*/http://mobilezonegt\.com(.*)", path)
    return real_path
