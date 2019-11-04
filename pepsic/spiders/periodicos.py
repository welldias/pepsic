# -*- coding: utf-8 -*-
import scrapy
import csv

class PeriodicosSpider(scrapy.Spider):

    name = 'periodicos'
    start_urls = ['http://pepsic.bvsalud.org/scielo.php?script=sci_alphabetic&lng=pt&nrm=iso']

    def parse_info(self, response):
        journalInfo = response.css('div.journalInfo')

        periodico = response.meta['periodico']
        periodico['publicador'] = journalInfo.css('strong.journalTitle::text').get(),
        periodico['issn'] = journalInfo.css('span.issn::text').get(),
        periodico['descricao'] = journalInfo.css('p font::text').get(),

        yield periodico

    def parse_numeros(self, response):

        edicoes = dict()
        edicoes['pid'] = response.meta['pid']
        for enum, linha in enumerate(response.css('html body div.content table tbody tr td table tbody tr')):
            if enum > 0:
                publicacoes = {
                    'ano' : linha.css('td p font b::text').get(),
                    'volume' : linha.css('td b font.normal::text').get(),
                }
                for numero in linha.css('a'):
                    publicacoes['numero_'+numero.css('::text').get()] =  numero.attrib['href']
                edicoes[enum] = publicacoes

        yield edicoes

    def parse(self, response):

        for periodico in response.css('li font.linkado'):
            link = periodico.css('a').attrib['href']
            link_periodicos = link.replace("script=sci_serial", "script=sci_issues")

            likParams  = dict((x.strip(), y.strip()) for x, y in (element.split('=') for element in link.split('&'))) 
            pid = likParams['pid']

            peri = {
                'pid' : pid,
                'link': link,
                'nome': " ".join(periodico.css('a::text').get().split()),
                'numeros': " ".join(filter(str.isdigit, periodico.css('font::text').get().replace("-","").split())),
            }

            yield scrapy.Request(link, meta={'periodico': peri}, callback=self.parse_info)
            yield scrapy.Request(link_periodicos, meta={'pid':pid}, callback=self.parse_numeros)
