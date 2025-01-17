# -*- coding: utf-8 -*-
import scrapy

class ArtigosSpider(scrapy.Spider):
    name = 'autores'
    start_urls = ['http://pepsic.bvsalud.org/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=article^dlibrary&index=AU&fmt=iso.pft&lang=p']
    author_name = None
    file_csv = None

    def print_authors(self, response):
        for nome in response.xpath('//select/option'):
            self.author_name = nome.attrib['value']
            self.file_csv.write(nome.attrib['value'])
            self.file_csv.write('\n')

    def parse(self, response):
        self.author_name = 'MARIA CLOTILDE ROSSETTI' #response.css('input[type="submit"]::attr(value)').extract_first()
        self.file_csv = open('data\\autors.csv', 'w')

        while True:                  
            params = {
                'IsisScript' :response.css('input[name="IsisScript"]::attr(value)').extract_first(),
                'environment':response.css('input[name="environment"]::attr(value)').extract_first(),
                'avaibleFormats':[
                    response.css('input[name="avaibleFormats"]::attr(value)')[0].get(),
                    response.css('input[name="avaibleFormats"]::attr(value)')[1].get(),
                    response.css('input[name="avaibleFormats"]::attr(value)')[2].get(),
                    response.css('input[name="avaibleFormats"]::attr(value)')[3].get(),
                ],
                'apperance':response.css('input[name="apperance"]::attr(value)').extract_first(),
                'helpInfo':response.css('input[name="helpInfo"]::attr(value)').extract_first(),
                'gizmoDecod':response.css('input[name="gizmoDecod"]::attr(value)').extract_first(),
                'avaibleForms':response.css('input[name="avaibleForms"]::attr(value)').extract_first(),
                'logoImage':response.css('input[name="logoImage"]::attr(value)').extract_first(),
                'logoURL':response.css('input[name="logoURL"]::attr(value)').extract_first(),
                'headerImage':response.css('input[name="headerImage"]::attr(value)').extract_first(),
                'headerURL':response.css('input[name="headerURL"]::attr(value)').extract_first(),
                'form':response.css('input[name="form"]::attr(value)').extract_first(),
                'pathImages':response.css('input[name="pathImages"]::attr(value)').extract_first(),
                'navBar':response.css('input[name="navBar"]::attr(value)').extract_first(),
                'hits':response.css('input[name="hits"]::attr(value)').extract_first(),
                'format':response.css('input[name="format"]::attr(value)').extract_first(),
                'lang':response.css('input[name="lang"]::attr(value)').extract_first(),
                'base':response.css('input[name="base"]::attr(value)').extract_first(),
                'exprSearch':response.css('input[name="exprSearch"]::attr(value)').extract_first(),
                'indexSearch':response.css('input[name="indexSearch"]::attr(value)').extract_first(),
                'termsFromIndex':response.css('input[name="termsFromIndex"]::attr(value)').extract_first(),
                'selectedIndex':response.css('input[name="selectedIndex"]::attr(value)').extract_first(),
                'user':response.css('input[name="user"]::attr(value)').extract_first(),
                'index':response.css('input[name="index"]::attr(value)').extract_first(),
                'baseFeatures':response.css('input[name="baseFeatures"]::attr(value)').extract_first(),
                'nextAction':response.css('input[name="nextAction"]::attr(value)').extract_first(),
                'indexRoot':[
                    '',
                    self.author_name,
                    ''
                ]
            }
            yield scrapy.FormRequest(
                'http://pepsic.bvsalud.org/cgi-bin/wxis.exe/iah/', 
                callback=self.print_authors, 
                method='POST', 
                formdata=params)