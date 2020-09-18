import scrapy

from scrapy.loader import ItemLoader
from zb.items import Doc, ZbItemLoader

import logging


class ZoobankSpider(scrapy.Spider):

    name = 'zoobank'
    allowed_domains = ['zoobank.org']

    start_urls = [
       'http://test.zoobank.org/Search?search_term=2010',
        'http://test.zoobank.org/Search?search_term=2011',
        'http://test.zoobank.org/Search?search_term=2012',
        'http://test.zoobank.org/Search?search_term=2013',
        'http://test.zoobank.org/Search?search_term=2014',
        'http://test.zoobank.org/Search?search_term=2015',
        'http://test.zoobank.org/Search?search_term=2016',
        'http://test.zoobank.org/Search?search_term=2017',
        'http://test.zoobank.org/Search?search_term=2018',
        'http://test.zoobank.org/Search?search_term=2019',
        'http://test.zoobank.org/Search?search_term=2020'
    ]

    yrs_list = ['2014', '2015', '2016', '2019', '2020']

    def parse(self, response):

        ol_element = 1

        if any(year in response.url for year in self.yrs_list):
            ol_element = 2
        elif '2018' in response.url:
            ol_element = 3

        r = response.xpath('//ol[@class="searchResults"][{}]//li'.format(ol_element))

        count_records = 0

        for sel in r:
            loader = ZbItemLoader(Doc(), selector=sel)
            loader.add_xpath('authors', 'descendant-or-self::*/text()')
            loader.add_xpath('year', 'descendant-or-self::*/text()')
            loader.add_xpath('title', 'descendant-or-self::*/text()')
            loader.add_xpath('journal', 'descendant-or-self::*/text()')
            loader.add_xpath('bibref_details', 'descendant-or-self::*/text()')
            loader.add_xpath('volume', 'descendant-or-self::*/text()')
            loader.add_xpath('issue', 'descendant-or-self::*/text()')
            loader.add_xpath('start_page', 'descendant-or-self::*/text()')
            loader.add_xpath('end_page', 'descendant-or-self::*/text()')
            loader.add_value('from_year', response.url[-4:])

            yield loader.load_item()
            #print(loader.load_item())      # Commented out for now

            count_records += 1

        log_message = "Total of {} records for year {}.".format(count_records,
            response.url[-4:])

        print(log_message)

        logging.warning(log_message)
