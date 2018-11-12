# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
'''
Author: Kris Shin
Edit Time: 18-11-11 21:43:53
'''
from pymongo import MongoClient


class MoviesMongoPipeline(object):
    def __init__(self, database):
        self.client = MongoClient()
        self.db = self.client[database]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(database=crawler.settings.get("DB_NAME"))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        movie = {}
        movie['mid'] = item['mid']
        movie['name'] = item['name']
        movie['date'] = item['date']
        movie['addr'] = item['addr']
        self.db.movies.insert(movie)
        return item
