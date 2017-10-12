# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider

from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor

import delorean

import logging

class OmpaAdSpider(scrapy.Spider):
    name = 'ompa.ad'
    allowed_domains = ['ompa.ad']
    start_urls = ['http://ompa.ad/bases_dades/dominis2.php']

    Rules= (Rule(LinkExtractor(allow=(), restrict_xpaths=('/html/body/table[2]/tbody/tr/td/span/p[2]/a',)), callback="parse", follow= True),)

    def parse(self, response):
        container_xpath = '//table'
        table_field = './tr/td/strong/text()'
        table_field_full = './tr/td'

        select_container = response.xpath(container_xpath)

        the_domains = []
        for a_table in select_container:
            # Bool to handle when to close a domain block
            close_a_domain_block = True

            # Initialize a_domain
            a_domain = {}

            print ()
            print ()
            print ()
            print ()

            for a_field in a_table.xpath(table_field_full):
                # Try to extract the title of each field of the table (tr/td)
                title = a_field.xpath("./strong/text()").extract_first()

                logging.debug (a_field)

                # Start parsing the fields of the table depending on the td text
                if title == "Nom de domini: ":
                    a_domain['domain'] = a_field.xpath("./a/text()").extract_first()
                elif title == "Titular: ":
                    a_domain['owner'] = a_field.xpath("./text()").extract_first()
                elif title and title.startswith("En base"):
                    a_domain['brand'] = a_field.xpath("./a/text()").extract_first().split(" ")[0]
                    a_domain['brand_url'] = a_field.xpath("./a/@href").extract_first()
                elif title and title.startswith("Data d'autoritzac"):
                    a_domain['creation_date'] = a_field.xpath("./text()").extract_first().replace(" ", "")
                    a_domain['creation_utc'] = delorean.parse(a_domain['creation_date']).epoch
                    close_a_domain_block = True

                # If a domain block parse is ended and resultant domain is not empty
                if close_a_domain_block and a_domain != {}:
                    the_domains.append(a_domain)
                    close_a_domain_block = False



        print (the_domains)
