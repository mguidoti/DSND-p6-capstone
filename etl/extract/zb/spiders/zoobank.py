import scrapy

from scrapy.loader import ItemLoader
from zb.items import Doc, ZbItemLoader


class ZoobankSpider(scrapy.Spider):

    name = 'zoobank'
    allowed_domains = ['zoobank.org']

    #start_urls = ['http://test.zoobank.org/Search?search_term=2018#publications']
    start_urls = ['file:///C:/Users/poa/Desktop/ZooBank.org.html']

    def parse(self, response):

        # TO DO: 2019 e 2020 needs to start at [2]
        r = response.xpath('//ol[@class="searchResults"][1]//li')
        #r = response.xpath('//ol[@class="searchResults"][1]//li/descendant-or-self::*/text()')

        count = 0

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

            loader.load_item()

            count += 1
            print(loader.item)

        print("\nTotal of... %s records." % count)
