# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from _datetime import datetime

from sqlalchemy.orm import sessionmaker

from shiyanlougithub.models import Repository, engine

class ShiyanlougithubPipeline(object):

    def process_item(self, item, spider):
        # "2017-06-07T00:27:11Z"
        item['update_time'] = datetime.strptime(item['update_time'], '%Y-%m-%dT%H:%M:%SZ')
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()