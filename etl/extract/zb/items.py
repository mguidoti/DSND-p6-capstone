# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, MapCompose, Join, TakeFirst

import re

class Doc(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    authors = scrapy.Field()
    year = scrapy.Field()
    title = scrapy.Field()
    journal = scrapy.Field()
    bibref_details = scrapy.Field()
    volume = scrapy.Field()
    issue = scrapy.Field()
    start_page = scrapy.Field()
    end_page = scrapy.Field()
    from_year = scrapy.Field()


def extract_bibref(string):

    string = string[re.search('[0-9]{4}', string).end():].strip().split('.')[1].strip()

    if re.search('[0-9]+', string) != None:
        return string[re.search('[0-9]+', string).start():]
    else:
        return ''


def extract_vol(string):

    if '(' in string:
        return string[:string.find('(')]
    elif ':' in string:
        return string[:string.find(':')]
    elif '-' not in string and '–' not in string:
        return string
    else:
        return ''



def extract_issue(string):

    issue = re.search('(?<=\()[0-9]+[\/|\-|\–]?[0-9]*(?=\))', string)

    if '(' in string and ')' in string and issue != None:
        return issue.group()
    else:
        return ''


def extract_start_page(string):

    page_range = string[string.find(':'):].strip()
    sep = re.search('[\-|\–]', page_range)

    if ':' in string and sep != None:
        return page_range[1:sep.start()].strip()

    elif ':' in string:
        return string[string.find(':'):].strip()

    else:
        return ''


def extract_end_page(string):

    page_range = string[string.find(':'):].strip()
    sep = re.search('[\-|\–]', page_range)

    if ':' in string and sep != None:
        return page_range[sep.start() + 1:]

    else:
        return ''


class ZbItemLoader(ItemLoader):

    default_input_processor = MapCompose(
        lambda x: "".join(x).replace('\n', '').replace('\t', '').replace('\r', ''),
        Join('')
    )

    authors_out = Compose(
        lambda x: "".join(x),
        lambda x: x[:re.search('[0-9]{4}', x).start()].strip()
    )

    year_out = Compose(
        Join(''),
        lambda x: re.search('[0-9]{4}', x).group()
    )

    title_out = Compose(
        Join(''),
        lambda x: x[re.search('[0-9]{4}', x).end():].strip().split('.')[0]
    )

    journal_out = Compose(
        Join(''),
        lambda x: x[re.search('[0-9]{4}', x).end():].strip().split('.')[1],
        lambda x: x[:re.search('[0-9]+', x).start()].strip() if re.search('[0-9]+', x) != None else x.strip()
    )

    bibref_details_out = Compose(
        Join(''),
        extract_bibref
    )

    volume_out = Compose(
        Join(''),
        extract_bibref,
        extract_vol
    )

    issue_out = Compose(
        Join(''),
        extract_bibref,
        extract_issue
    )

    start_page_out = Compose(
        Join(''),
        extract_bibref,
        extract_start_page
    )

    end_page_out = Compose(
        Join(''),
        extract_bibref,
        extract_end_page
    )

    from_year_out = Compose(TakeFirst())