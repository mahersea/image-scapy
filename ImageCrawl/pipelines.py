# -*- coding: utf-8 -*-
# coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import MySQLdb
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline

from ImageCrawl.items import ImageItem
import sys

reload(sys)

sys.setdefaultencoding('utf-8')


class AdultVideoPipeline(object):
    def __init__(self, dbargs):
        self.db_settings = dbargs
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['MYSQL_DATABASE'])

    def open_spider(self, spider):
        try:
            self.db = MySQLdb.connect(
                host=self.db_settings['host'],
                port=self.db_settings['port'],
                user=self.db_settings['user'],
                passwd=self.db_settings['password'],
                db=self.db_settings['name'],
                charset="utf8")
        except Exception as e:
            logging.warn('[chengz]: mysql connect failed, details:'+ e.message)

    def close_spider(self, spider):
        logging.info('[chengz]: spider stop at page: %s' % spider.last_page)
        if self.db:
            self.db.close()

    def process_item(self, item, spider):
        if not item or not item['tid']:
            return
        try:
            cur = self.db.cursor()
            query_sql = 'select * from porn_adultvideo where tid=%s' % item['tid']
            cur.execute(query_sql)
            if not cur.fetchone():
                sql = "insert into porn_adultvideo(tid,title,cover_image,link_url) VALUES (%s,%s,%s,%s)"
                cur.execute(sql, (item['tid'], item['title'], item['url'], item['link_url']))
                self.db.commit()
        except Exception as e:
            logging.warn("mysql error: %" % e.message)
        finally:
            cur.close()


# class ImagesDownloadPipeline(ImagesPipeline):
#     dbargs = None

#     def file_path(self, request, response=None, info=None):
#         image_file_name = request.url.split('/')[-1]
#         return '%s' % image_file_name

#     def get_media_requests(self, item, info):
#         if isinstance(item, ImageItem) and item['url']:
#             yield Request(item['url'])

#     @classmethod
#     def from_settings(cls, settings):
#         cls.dbargs = settings['MYSQL_DATABASE']
#         return super(ImagesDownloadPipeline, cls).from_settings(settings)

#     def open_spider(self, spider):
#         try:
#             self.connection = MySQLdb.connect(
#                 host=self.dbargs['host'],
#                 port=self.dbargs['port'],
#                 user=self.dbargs['user'],
#                 passwd=self.dbargs['password'],
#                 db=self.dbargs['name'],
#                 charset="utf8")
#         except Exception as e:
#             logging.warn(e.message)
#         super(ImagesDownloadPipeline, self).open_spider(spider)

#     def close_spider(self, spider):
#         logging.info('[chengz]: spider stop at page: %s' % spider.last_page)
#         if self.connection:
#             self.connection.close()
#         super(ImagesDownloadPipeline, self).close_spider(spider)

#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         if not image_paths:
#             raise DropItem("Item contains no images")
#         try:
#             cur = self.connection.cursor()
#             sql = "insert into porn_adultvideo(title,cover_image,link_url) VALUES (%s,%s,%s)"
#             cur.execute(sql, (item['title'], item['url'], item['link_url']))
#             self.connection.commit()
#         except Exception as e:
#             logging.warn("mysql error: %" % e.message)
#         finally:
#             cur.close()
#         return item
