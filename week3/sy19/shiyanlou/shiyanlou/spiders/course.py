# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import CourseItem

class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['shiyanlou.com']
    start_urls = ['http://shiyanlou.com/']

    @property
    def start_urls(self):
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))

    def parse(self, response):

        for course in response.xpath("//div[contains(@class, 'course-body')]"):
                # 使用 xpath 语法对每个 course 提取数据
            yield CourseItem({
                # 课程名称
                'name': course.xpath('.//div[contains(@class, "course-name")]/text()').extract_first(default="未知"),
                # 课程描述
                'description': course.xpath('.//div[contains(@class, "course-desc")]/text()').extract_first(default="空"),
                # 课程类型，实验楼的课程有免费，会员，训练营三种，免费课程并没有字样显示，也就是说没有 span.pull-right 这个标签，没有这个标签就代表时免费课程，使用默认值 `免费｀就可以了。

                'type':course.xpath(
                './/div[contains(@class, "course-footer")]/span[contains(@class, "pull-right")]/text()').extract_first(
                default="免费"),
                # 注意 // 前面的 .，没有点表示整个文档所有的 div.course-body，有 . 才表示当前迭代的这个 div.course-body
                'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first(
                    '[^\d]*(\d*)[^\d]*')
            })
