# -*- coding: utf-8 -*-
'''
Author: Kris Shin
Edit Time: 18-11-11 16:16:44
'''
import time, re
from scrapy import Request, Spider
from spider_movies.items import SpiderMoviesItem


class S80SpiderSpider(Spider):
    name = 'S80_spider'
    allowed_domains = ['www.80s.tw']
    start_urls = ['http://www.80s.tw/']

    def start_requests(self):
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
        for i in range(1):
            yield Request(
                url='https://www.80s.tw/movie/list/-----p/%s' % str(i + 1),
                headers=headers,
                method='GET',
                callback=self.parse_list)

    def parse_list(self, response):
        items = response.selector.xpath('//ul[@class="me1 clearfix"]//li')

        for item in items:
            time.sleep(2)
            film = SpiderMoviesItem()
            film['mid'] = item.xpath('./h3/a/@href').extract_first().split(
                '/')[-1]
            film['name'] = item.xpath('./h3/a/text()').extract_first().strip()
            url = S80SpiderSpider.start_urls[0][:-1] + item.xpath(
                './h3/a/@href').extract_first()
            yield Request(
                url=url, meta={'film': film}, callback=self.parse__date_addr)

    def parse__date_addr(self, response):
        film = response.meta['film']
        # film['date'] = response.selector.xpath(
        #     '//div[@class="info"]/div[@class="clearfix"]//span//text()'
        # ).extract()
        re_date = '上映日期：</span>"(\d{4}-\d{2}-\d{2}"'
        data = re.match(re_date, response.text).groups()
        print(data)
        # film['addr'] = response.selector.xpath(
        #     '//div[@id="cpdl2list"]//li//span[@class="xunlei dlbutton1"]/a/@href'
        # ).extract_first()
        # yield film
