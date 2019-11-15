# -*- coding: utf-8 -*-
import scrapy
import csv

class DownloadArtigosSpider(scrapy.Spider):
    name = 'download_artigos'
    start_urls = ['http://pepsic.bvsalud.org/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=article%5Edlibrary&fmt=iso.pft&lang=p']

    def list_articles(self, response):
        for link in response.xpath('/html//a[@class="isoref"]'):
            if 'script=sci_arttext' in link.attrib['href']:
                yield {
                    'autor': response.meta['author_name'],
                    'link': link.attrib['href'],
                }

    def parse(self, response):
        #author_name = 'OLIVER ZANCUL'
        file_name = 'data\\autors.csv'
        with open(file_name) as fp:
            for line in fp:
                author_name = line.rstrip()
                params = {
                    'IsisScript': response.css('input[name="IsisScript"]::attr(value)').extract_first(),
                    'environment': response.css('input[name="environment"]::attr(value)').extract_first(),
                    'avaibleFormats': [
                        response.css('input[name="avaibleFormats"]::attr(value)')[0].get(),
                        response.css('input[name="avaibleFormats"]::attr(value)')[1].get(),
                        response.css('input[name="avaibleFormats"]::attr(value)')[2].get(),
                        response.css('input[name="avaibleFormats"]::attr(value)')[3].get(),
                    ],
                    'apperance': response.css('input[name="apperance"]::attr(value)').extract_first(),
                    'helpInfo': response.css('input[name="helpInfo"]::attr(value)').extract_first(),
                    'gizmoDecod': response.css('input[name="gizmoDecod"]::attr(value)').extract_first(),
                    'avaibleForms': response.css('input[name="avaibleForms"]::attr(value)').extract_first(),
                    'logoImage': response.css('input[name="logoImage"]::attr(value)').extract_first(),
                    'logoURL': response.css('input[name="logoURL"]::attr(value)').extract_first(),
                    'headerImage': response.css('input[name="headerImage"]::attr(value)').extract_first(),
                    'headerURL': response.css('input[name="headerURL"]::attr(value)').extract_first(),
                    'form': response.css('input[name="form"]::attr(value)').extract_first(),
                    'pathImages': response.css('input[name="pathImages"]::attr(value)').extract_first(),
                    'navBar': response.css('input[name="navBar"]::attr(value)').extract_first(),
                    'hits': response.css('input[name="hits"]::attr(value)').extract_first(),
                    'format': response.css('input[name="format"]::attr(value)').extract_first(),
                    'lang': response.css('input[name="lang"]::attr(value)').extract_first(),
                    'user': response.css('input[name="user"]::attr(value)').extract_first(),
                    'baseFeatures': response.css('input[name="baseFeatures"]::attr(value)').extract_first(),
                    'nextAction': response.css('input[name="nextAction"]::attr(value)').extract_first(),
                    'base': response.css('input[name="base"]::attr(value)').extract_first(),
                    'conectSearch': ['init', 'and', 'and'],
                    'exprSearch': [ author_name, '', '', ],
                    'indexSearch': [
                        '^nAu^pAutor^eAutor^iAuthor^xAU ^yPREINV^uAU_^mAU_',
                        '^nTo^pTodos os índices^eTodos los indices^iAll indexes^d*^xTO ^yFULINV',
                        '^nTo^pTodos os índices^eTodos los indices^iAll indexes^d*^xTO ^yFULINV',
                    ],
                    'x': '20',
                    'y': '8',
                }
                yield scrapy.FormRequest(
                    'http://pepsic.bvsalud.org/cgi-bin/wxis.exe/iah/', 
                    callback=self.list_articles, 
                    method='POST', 
                    formdata=params,
                    meta={'author_name':author_name})
