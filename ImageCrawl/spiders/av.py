# -*- coding: utf-8 -*-
# coding=utf-8
import re
import sys

import scrapy

from ImageCrawl.items import ImageItem

reload(sys)

sys.setdefaultencoding('utf-8')


class AvSpider(scrapy.Spider):
    name = 'av'
    domain = 'http://x77125.com/bbs/'
    count = 0
    max_page = 5
    last_page = -1
    start_page = 30
    start_urls = [
        'http://x77125.com/bbs/thread.php?fid=20&page=%s' % start_page,
        # 'http://x77125.com/bbs/thread.php?fid=7&page=%s' % start_page
    ]

    def parse(self, response):
        for subject_url in response.css('#threadlist .subject a::attr(href)').extract():
            if 'http' not in subject_url:
                link_url = self.domain + subject_url
            else:
                link_url = subject_url
            yield response.follow(link_url, self.parse_subject)

        page_char_pos = response.url.find('page')
        if page_char_pos is -1:
            page_index = 1
            next_page = '%s&page=%s' % (response.url, page_index + 1)
        else:
            page_index = int(response.url[page_char_pos + 5:])
            next_page = response.url.replace('page=%s' % page_index, 'page=%s' % (page_index + 1))

        if next_page and self.count < self.max_page:
            self.count += 1
            if page_index > self.last_page:
                self.last_page = page_index

            yield response.follow(next_page, self.parse)

    def parse_subject(self, response):
        match = re.search(r'tid=(?P<tid>\d+)', response.url)
        if not match or not match.group('tid') or not match.group('tid').isdigit():
            return
        tid = int(match.group('tid'))
        title = response.css('#subject_tpc::text').extract()[1]
        image_url = response.css('#read_tpc img::attr(src)').extract_first()
        yield ImageItem(tid=tid, url=image_url, title=title, link_url=response.url)
