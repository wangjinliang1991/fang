# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from .items import NewhouseItem,ESFItem
import pymongo

class FangPipeline(object):
    def __init__(self):
        self.newhouse_fp = open('newhouse.json','wb')
        self.esf_fp = open('esf.json','wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
        self.esf_exporter = JsonLinesItemExporter(self.esf_fp,ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item,NewhouseItem):
            self.newhouse_exporter.export_item(item)
        elif isinstance(item,ESFItem):
            self.esf_exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.newhouse_fp.close()
        self.esf_fp.close()


class MongoPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.db[NewhouseItem.collection].create_index([('id',pymongo.ASCENDING)])
        self.db[ESFItem.collection].create_index([('id',pymongo.ASCENDING)])

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        if isinstance(item,NewhouseItem) or isinstance(item,ESFItem):
            self.db[item.collection].insert(dict(item))
        return item
