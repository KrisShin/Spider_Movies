# -*- coding: utf-8 -*-
'''
Author: Kris Shin
Edit Time: 18-11-11 20:11:17
'''
import time
import scrapy

from spider_movies.items import SpiderMoviesItem


class YgSpiderSpider(scrapy.Spider):
    name = 'YG_spider'
    allowed_domains = ['ygdy8.com']
    start_urls = ['http://ygdy8.com']

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
        for page in range(170):
            time.sleep(1)
            yield scrapy.Request(
                url='http://www.ygdy8.com/html/gndy/dyzz/list_23_%s.html' %
                str(page + 1),  # %key_word,
                headers=headers,
                method='GET',
                callback=self.parse)

    def parse(self, response):
        # get all movies
        movies = response.selector.xpath('//ul//table[@class="tbspan"]')

        for movie in movies:
            film = SpiderMoviesItem()
            id_date = movie.xpath('.//tr//td/b/a/@href').extract_first()
            film['mid'] = id_date.split('/')[-1].split('.')[-2]
            film['name'] = movie.xpath('.//tr//td/b/a/text()').extract_first()
            film['date'] = id_date.split('/')[-2]
            url = 'http://ygdy8.com' + id_date
            yield scrapy.Request(
                url=url, meta={'film': film}, callback=self.parse_addr)

    def parse_addr(self, response):
        film = response.meta['film']
        film['addr'] = response.selector.xpath(
            '//div[@class="co_content8"]//a/@href').extract_first().strip()
        yield film
