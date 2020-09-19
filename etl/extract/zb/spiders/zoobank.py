import scrapy

from scrapy.loader import ItemLoader
from zb.items import Doc, ZbItemLoader

import logging


class ZoobankSpider(scrapy.Spider):
    """Spider that will do the crawling on the provided start_urls

    Args:
        scrapy (Class): Class scrapy.Spider, inherits from it

    Yields:
        scrapy.Item: [description]
    """

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

    # This website is might vary the quantity of <ol> elemnet, and I'm only
    # interested in one, which order might vary as well. Thus, I created this
    # list, to help set the right integer that will find the right element on
    # the xpath
    yrs_list = ['2014', '2015', '2016', '2019', '2020']

    def parse(self, response):

        # This is the start of the logic to define which <ol> element I should
        # take, depending on the year that I'm querying the system. By default
        # I'm setting it as 1
        ol_element = 1

        # If any of the years on the list yrs_list, then, set it as 2
        if any(year in response.url for year in self.yrs_list):
            ol_element = 2
        # If it's specifically '2018', then set it as 3
        elif '2018' in response.url:
            ol_element = 3

        # Pass the xpath with the variable ol_element, and get selectors as re-
        # turn
        r = response.xpath('//ol[@class="searchResults"][{}]//li'.format(ol_element))

        count_records = 0

        # For each returning selector, define a ItemLoader based on the custom
        # ItemLoader on etl.extract.zb.items.py and pass all information to be
        # processed by my custom ItemPipeline and in- and out-processors
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
            #print(loader.load_item())      # Commented out for now, but useful

            count_records += 1

        # Creates a message to be logged and printed on the terminal
        log_message = "Total of {} records for year {}.".format(count_records,
            response.url[-4:])

        print(log_message)
        logging.warning(log_message)
