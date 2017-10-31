import scrapy

class ShiyanlouCoursesSpider(scrapy.Spider):
    """ 所有 scrpy 爬虫需要写一个 Spider 类，这个类要继承 scrapy.Spider 类。在这个类中定义要请求的网站和链接、如何从返回的网页提取数据等等。
    """

    # 爬虫标识符号，在 scrapy 项目中可能会有多个爬虫，name 用于标识每个爬虫，不能相同
    name = 'shiyanlou-courses'


    # 我们只负责提供url
    @property
    def start_urls(self):
        """ start_urls 需要是一个可迭代对象，所以，你可以把它写成一个列表、集合或者生成器，这里用的是生成器
        """
        url_tmpl = 'https://github.com/shiyanlou?tab=repositories@page={}'
        return (url_tmpl.format(i) for i in range(1, 4))


    def parse(self, response):
        """ 这个方法作为 `scrapy.Request` 的 callback，在里面编写提取数据的代码。scrapy 中的下载器会下载 `start_reqeusts` 中定义的每个 `Request` 并且结果封装为一个 response 对象传入这个方法。
        """

        # CSS
        # 遍历每个课程的 div.course-body
        # for course in response.css('div.course-body'):
        #     # 使用 css 语法对每个 course 提取数据
        #     yield {
        #         # 课程名称
        #         'name': course.css('div.course-name::text').extract_first(),
        #         # 课程描述
        #         'description': course.css('div.course-desc::text').extract_first(),
        #         # 课程类型，实验楼的课程有免费，会员，训练营三种，免费课程并没有字样显示，也就是说没有 span.pull-right 这个标签，没有这个标签就代表时免费课程，使用默认值 `免费｀就可以了。
        #         'type': course.css('div.course-footer span.pull-right::text').extract_first(default='免费'),
        #         # 注意 // 前面的 .，没有点表示整个文档所有的 div.course-body，有 . 才表示当前迭代的这个 div.course-body
        #         'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first(
        #             '[^\d]*(\d*)[^\d]*')
        #     }

        # XPATH
        for course in response.xpath("//div[contains(@class, 'course-body')]"):
                # 使用 xpath 语法对每个 course 提取数据
            yield {
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
            }