# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker

from shiyanlou.models import Course, engine


class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item["student"] = int(item["student"])
        return item

    def open_spider(self, spider):
        Session = sessionmaker(engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()


