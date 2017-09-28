import scrapy

from ImageCrawl.items import ImageItem


class X77ImageSpider(scrapy.Spider):
    name = "X77Image"
    domain = 'http://x77125.com/bbs/'
    start_urls = [
        'http://x77125.com/bbs/thread.php?fid=6'
    ]

    def parse(self, response):
        for subject_url in response.css('.subject a::attr(href)').extract():
            if 'http' not in subject_url:
                link_url = self.domain + subject_url
            else:
                link_url = subject_url
            yield response.follow(link_url, self.parse_subject)

    def parse_subject(self, response):
        image_url = response.css('#read_tpc img::attr(src)').extract_first()
        yield ImageItem(url=image_url)
