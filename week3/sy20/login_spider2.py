#coding=utf-8

import scrapy
from bs4 import BeautifulSoup

class LoginSpiderSpider(scrapy.Spider):

    name = "login_spider"
    start_urls = ["https://www.shiyanlou.com/login"]

    def parse(self, response):
        """
        1. get login page
        2. get cookies
        3. create request
        4.FormRequest  make post

        """
        csrf_token = response.xpath('//div[@class="login-body"]//input[@id="csrf_token"]/@value').extract_first()
        self.logger.info(csrf_token)
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'csrf_token': csrf_token,
                'login': 'wuqize5109@163.com',
                'password': '676077Wu',
            },
            callback=self.after_login
        )

    def after_login(self, response):
        return [scrapy.Request(
            url='https://www.shiyanlou.com/user/259134/',
            callback=self.parse_after_login
        )]

    def parse_after_login(self, response):
        print("==================")
        soup = BeautifulSoup(response.body)
        print(soup.find_all("span", class_="info-text"))
        yield  {
            'lab_count': response.xpath('(//span[@class="info-text"])[2]/text()'),#.re_first('[^\d]*(\d*)[^\d*]'),
            'lab_minutes': response.xpath('(//span[@class="info-text"])[3]/text()'),#.re_first('[^\d]*(\d*)[^\d*]')
        }
        """
        :nth-child(1) > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > span
        """