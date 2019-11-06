# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.loader import ItemLoader
from pepsic.items import PepsicItem

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

    def artigo_salva(self, response):
        temp = (response.url.split('?')[-1])
        temp = dict((x.strip(), y.strip()) for x, y in (element.split('=') for element in temp.split('&'))) 
        
        nome_arquivo = temp['pid']
        tipo = response.meta['tipo']
        path_file = 'data\\{}\\{}.{}'.format(tipo, nome_arquivo, tipo)
        
        self.logger.info('Salvando arquivo %s', path_file)
        with open(path_file, 'wb') as f:
            f.write(response.body)

    def salva_arquivo(self, response):
        loader = ItemLoader(item=PepsicItem(), selector=response.url)
        loader.add_value('file_urls', response.url)
        yield loader.load_item()

    def artigo_info(self, response):
        nome_periodico = ' '.join(response.css('html body div.container div.content h2 a::text').get().split())
        info_periodico = ' '.join(response.css('html body div.container div.content h3::text').get().split())
        link_pdf = response.urljoin(response.xpath('/html//a[contains (text(),"pdf")]').attrib['href'])
        link_xml = response.xpath('/html//a[@target="xml"]').attrib['href']

        #yield scrapy.Request(link_xml, meta={'tipo':'xml'}, callback=self.artigo_salva)
        #yield scrapy.Request(link_pdf, meta={'tipo':'pdf'}, callback=self.artigo_salva)
        yield scrapy.Request(link_pdf, callback=self.salva_arquivo)
        yield scrapy.Request(link_xml, callback=self.salva_arquivo)
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
