# -*- coding: utf-8 -*-

import pymongo
from meizi.items import MzItem, UmeiItem, Win4000Item, A7160Item

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



class MongoPipeline(object):

    Mz_collection_name = 'MZ'
    Umei_collection_name = 'Umei'
    Win4000_collection_name = 'Win4000'
    A7160_collection_name = 'A7160'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, MzItem):
            self.db[self.Mz_collection_name].update({'title_url':item['title_url']},{'$set': item}, True)
            print('保存到mongodb成功\n')
            return item
        if isinstance(item, UmeiItem):
            self.db[self.Umei_collection_name].update({'title_url':item['title_url']},{'$set': item}, True)
            print('保存到mongodb成功\n')
            return item
        if isinstance(item, Win4000Item):
            self.db[self.Win4000_collection_name].update({'title_url':item['title_url']},{'$set': item}, True)
            print('保存到mongodb成功\n')
            return item
        if isinstance(item, A7160Item):
            self.db[self.A7160_collection_name].update({'title_url':item['title_url']},{'$set': item}, True)
            print('保存到mongodb成功\n')
            return item