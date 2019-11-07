# -*- coding: utf-8 -*-
import scrapy
import csv
import glob
import os

class DownloadPeriodicosSpider(scrapy.Spider):
    name = 'download_periodicos'

    def start_requests(self):
        pid = getattr(self, 'pid', None)

        if pid:
            csv_file_name = 'data\\periodicos-{}.csv'.format(pid)
            with open(csv_file_name) as csv_file:
                csv_file_reader = csv.reader(csv_file, delimiter=',')
                for enum, linha in enumerate(csv_file_reader):
                    if enum > 0:
                        yield scrapy.Request(linha[4])
        else:
            for file in os.listdir('data\\'):
                if file.startswith('periodicos'):
                    csv_file_name = 'data\\{}'.format(file)
                    with open(csv_file_name) as csv_file:
                        csv_file_reader = csv.reader(csv_file, delimiter=',')
                        for enum, linha in enumerate(csv_file_reader):
                            if enum > 0:
                                yield scrapy.Request(linha[4])


    def salvar_arquivo(self, response):
        file_name = None
        if response.url.endswith('.pdf'):
            file_name = response.url.split('/')[-1]
        elif 'articleXML.php' in response.url:
            temp = (response.url.split('?')[-1])
            temp = dict((x.strip(), y.strip()) for x, y in (element.split('=') for element in temp.split('&'))) 
            file_name = '{}.{}'.format(temp['pid'], 'xml')
        
        if file_name:
            path_file = 'data\\files\\{}'.format(file_name)
            with open(path_file, 'wb') as f:
                f.write(response.body)

    def artigo_info(self, response):
        nome_periodico = ' '.join(response.css('html body div.container div.content h2 a::text').get().split())
        info_periodico = ' '.join(response.css('html body div.container div.content h3::text').get().split())
        link_pdf = response.urljoin(response.xpath('/html//a[contains (text(),"pdf")]').attrib['href'])
        link_xml = response.xpath('/html//a[@target="xml"]').attrib['href']

        yield scrapy.Request(link_xml, callback=self.salvar_arquivo)
        yield scrapy.Request(link_pdf, callback=self.salvar_arquivo)
        yield {
            'nome periodico' : nome_periodico,
            'info periodico' : info_periodico,
            'link pdf' : link_pdf,
            'link xml' : link_xml,
        }

    def parse(self, response):
        for artigo in response.css('html body div.content table tbody tr td table tbody tr td div a'):
            if 'script=sci_arttext' in artigo.attrib['href']:
                yield scrapy.Request(artigo.attrib['href'], callback=self.artigo_info)
