# -*- coding: utf-8 -*-
import scrapy
import csv

class DownloadPeriodicosSpider(scrapy.Spider):
    name = 'download_periodicos'

    def start_requests(self):
        pid = getattr(self, 'pid', None)
        csv_file_name = 'data\\periodicos-{}.csv'.format(pid)
        
        with open(csv_file_name) as csv_file:
            csv_file_reader = csv.reader(csv_file, delimiter=',')
            for enum, linha in enumerate(csv_file_reader):
                if enum > 0:
                    yield scrapy.Request(linha[4])

    def parse(self, response):
        yield {
          'sumario' : response.css('html body div.content table tbody tr td table tbody tr td div a').get(),
        } 
