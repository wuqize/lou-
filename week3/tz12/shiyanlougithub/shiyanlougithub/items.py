# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShiyanlougithubItem(scrapy.Item):
    # define the fields for your item here like:
    # define the fields for your item here like:
    name = scrapy.Field()
    update_time = scrapy.Field()
    branches = scrapy.Field()
    commits = scrapy.Field()
    releases = scrapy.Field()