# -*- coding: utf-8 -*-
import scrapy

from shiyanlougithub.items import ShiyanlougithubItem

class ShiyanlougithubSpider(scrapy.Spider):
    name = 'shiyanlougithub'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?tab=repositories&page={}'
        return (url_tmpl.format(i) for i in range(1, 5))


    def parse(self, response):
        for repo in response.xpath("//ul[contains(@data-filterable-type, 'substring')]/li"):
                # 使用 xpath 语法对每个 course 提取数据
            item = ShiyanlougithubItem({
                "name": repo.xpath(".//div[1]/h3/a/text()").re_first('[\n ]*([\d\w]*)[\n ]*'),
                "update_time": repo.xpath(".//div[3]/relative-time/@datetime").extract_first()
            })
            repo_url = response.urljoin(repository.xpath('.//a/@href').extract_first())
            request = scrapy.Request(repo_url, callback=self.parse_repo)
            request.meta['item'] = item
            yield request

    def parse_repo(self, response):
        item = response.meta['item']
        for li in response.xpath(".//ul[contains(@class,'numbers-summary')]"):
            which = li.xpath(".//a/text()").extarct_first().strip("\n").strip()
            number = li.xpath('.//a/span[@class="num text-emphasized"]/text()').strip("\n").strip().replace(',', '')
            name_dict = {"comm":"commits", "bran":"branchs","rele":"releases"}
            item[name_dict[which[:4]]] = int(number)
        yield item