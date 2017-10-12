# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider

from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class OmpaAdSpider(scrapy.Spider):
    name = 'ompa.ad'
    allowed_domains = ['ompa.ad']
    start_urls = ['http://ompa.ad/bases_dades/dominis2.php']

    Rules= (Rule(LinkExtractor(allow=(), restrict_xpaths=('/html/body/table[2]/tbody/tr/td/span/p[2]/a',)), callback="parse", follow= True),)


    def parse(self, response):
        pass
