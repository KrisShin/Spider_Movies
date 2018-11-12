# -*- coding: utf-8 -*-
'''
Author: Kris Shin
Edit Time: 18-11-11 16:16:44
'''
from scrapy import Request, Spider


class S80SpiderSpider(Spider):
    name = 'S80_spider'
    allowed_domains = ['80s.tw']
    start_urls = ['http://80s.tw/']

    def start_requests(self):
        pass

    def parse(self, response):
        pass
