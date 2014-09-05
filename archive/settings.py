# Scrapy settings for archive project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'archive'
#BOT_VERSION = '1.0'

SPIDER_MODULES = ['archive.spiders']
NEWSPIDER_MODULE = 'archive.spiders'
USER_AGENT = '%s' % (BOT_NAME)

ITEM_PIPELINES = [
        'archive.pipelines.PagePipeline',
        ]

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = './error.log'
LOG_LEVEL = 'ERROR'
LOG_STDOUT = True
