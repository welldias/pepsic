# -*- coding: utf-8 -*-
import scrapy


class ArtigosSpider(scrapy.Spider):
    name = 'artigos'
    start_urls = ['']

    def parse(self, response):
        pass


