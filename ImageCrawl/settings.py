# -*- coding: utf-8 -*-

# Scrapy settings for ImageCrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ImageCrawl'

SPIDER_MODULES = ['ImageCrawl.spiders']
NEWSPIDER_MODULE = 'ImageCrawl.spiders'

ITEM_PIPELINES = {
    'ImageCrawl.pipelines.AdultVideoPipeline': 301,
}

IMAGES_STORE = '/Users/Orange/Desktop/Image'

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 16

RETRY_TIMES = 3

MYSQL_DATABASE = {
    'name': 'orangeDB',
    'user': 'root',
    'password': 'cheng123',
    'host': '127.0.0.1',
    'port': 3306
}
