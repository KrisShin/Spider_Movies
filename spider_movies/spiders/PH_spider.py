# -*- coding: utf-8 -*-
'''
Author: Kris Shin
Edit Time: 18-11-11 03:51:27
'''
from scrapy import Request, Spider

from spider_movies.items import SpiderMoviesItem


class PhSpiderSpider(Spider):
    name = 'PH_spider'
    allowed_domains = ['xpiaohua.com']
    start_urls = ['http://xpiaohua.com/']

    def start_requests(self):
        # set header to cover spider
        headers = {
            'User-Agent':
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept':
            'application/json, text/plain, */*',
            'Accept-Encoding':
            'gzip, deflate, sdch',
            'Accept-Language':
            'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection':
            'keep-alive',
            'X-Requested-With':
            'XMLHttpRequest',
            'Content-Type':
            'application/x-www-form-urlencoded; charset=UTF-8'
        }
        # key_word = input('Please input file name:\n>>>')  # set search word here
        yield Request(
            url='http://www.xpiaohua.com/',
            headers=headers,
            method='GET',
            callback=self.parse_cate)

    def parse_cate(self, response):
        menus = response.selector.xpath(
            '//div[@id="menu"]/ul/li/a/@href').extract()
        menus = menus[1:10]
        for menu in menus:
            # per category movies about 59 pages
            for i in range(59):
                yield Request(
                    url=menu + '/list_%s.html' % str(i + 1),
                    callback=self.parse_info)

    def parse_info(self, response):
        items = response.selector.xpath('//div[@id="list"]/dl/dd')
        for item in items:
            film = SpiderMoviesItem()
            url = item.xpath('./strong/a/@href').extract_first()
            film['mid'] = url.split('/')[-1].split('.')[0]
            film['name'] = item.xpath('./strong/a/text()').extract_first()
            film['date'] = item.xpath(
                './span/text()').extract_first().strip().split('：')[-1]
            yield Request(
                url=url, meta={'film': film}, callback=self.parse_addr)

    def parse_addr(self, response):
        film = response.meta['film']
        film['addr'] = response.selector.xpath(
            '//div[@id="showinfo"]//a/@href').extract()
        yield film
