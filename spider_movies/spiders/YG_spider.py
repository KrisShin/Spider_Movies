# -*- coding: utf-8 -*-
'''
Author: Kris Shin
Edit Time: 18-11-11 20:11:17
'''
import scrapy


class YgSpiderSpider(scrapy.Spider):
    name = 'YG_spider'
    allowed_domains = ['ygdy8.com']
    start_urls = ['http://ygdy8.com']

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
        key_word = input('Please input file name:\n>>>')
        return scrapy.Request(
            url='http://s.ygdy8.com/plus/so.php?typeid=1&keyword=%s' %
            key_word,
            headers=headers,
            method='GET',
            callback=self.parse,
        )

    def parse(self, response):
        print(response.text)
