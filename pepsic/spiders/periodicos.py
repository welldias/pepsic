# -*- coding: utf-8 -*-
import scrapy
import csv

class PeriodicosSpider(scrapy.Spider):

    name = 'periodicos'
    start_urls = ['http://pepsic.bvsalud.org/scielo.php?script=sci_alphabetic&lng=pt&nrm=iso']

    def parse_info(self, response):
        journalInfo = response.css('div.journalInfo')

        periodico = response.meta['periodico']

        csv_file_name = 'data\\periodicos.csv'
        with open(csv_file_name, mode='a', newline='') as csv_file:
            csv_file_writer = csv.writer(csv_file, delimiter=',')
            info = [
                periodico[0],
                periodico[1],
                periodico[2],
                periodico[3],
                journalInfo.css('strong.journalTitle::text').get(),
                journalInfo.css('span.issn::text').get(),
                journalInfo.css('p font::text').get(),
            ]
            csv_file_writer.writerow(info)

        #yield periodico

    def parse_numeros(self, response):
        pid = response.meta['pid']

        csv_file_name = 'data\\periodicos-{}.csv'.format(pid)
        with open(csv_file_name, mode='w', newline='') as csv_file:
            csv_file_writer = csv.writer(csv_file, delimiter=',')
            csv_file_writer.writerow(['pid', 'ano', 'volume', 'numero', 'link'])
            for enum, linha in enumerate(response.css('html body div.content table tbody tr td table tbody tr')):
                if enum > 0:
                    for numero in linha.css('a'):
                        edicao = [
                                pid,
                                linha.css('td p font b::text').get(), #ano
                                linha.css('td b font.normal::text').get(), #volume
                                numero.css('::text').get(), #numero
                                numero.attrib['href'], #link
                        ]
                        csv_file_writer.writerow(edicao)
        #yield numeros_issn

    def parse(self, response):
        for periodico in response.css('li font.linkado'):
            #periodico = response.css('li font.linkado')[0]
            link = periodico.css('a').attrib['href']
            link_periodicos = link.replace("script=sci_serial", "script=sci_issues")

            likParams  = dict((x.strip(), y.strip()) for x, y in (element.split('=') for element in link.split('&'))) 
            pid = likParams['pid']

            peri = [
                pid,
                link,
                ' '.join(periodico.css('a::text').get().split()),
                ' '.join(filter(str.isdigit, periodico.css('font::text').get().replace("-","").split())),
            ]

            yield scrapy.Request(link_periodicos, meta={'pid':pid}, callback=self.parse_numeros)
            yield scrapy.Request(link, meta={'periodico': peri}, callback=self.parse_info)

