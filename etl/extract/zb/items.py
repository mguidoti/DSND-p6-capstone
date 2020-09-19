# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, MapCompose, Join, TakeFirst

import re

class Doc(scrapy.Item):
    """Create Item Class which objets will contain the information passing
    through the Item Pipeline

    Args:
        scrapy.Item (Class): Class scrapy.Item
    """
    # Defining all scrapy.Fields
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
    """Extracts bibliographic information, returning volume(issue): page-range
    if they are all present. If they are not, return what is available.

    Args:
        string (str): String being passed by the Item Pipeline

    Returns:
        str: String with the entire bibref information
    """

    # After the year (regex), grab the remaining characters and split on period.
    # Then get the second element on the resulting list
    string = string[re.search('[0-9]{4}', string).end():].strip().split('.')[1].strip()

    # Test if there are numbers left
    if re.search('[0-9]+', string) != None:
        # If so, return from its start
        return string[re.search('[0-9]+', string).start():]
    else:
        # If there are no numbers left, return an empty string
        return ''


def extract_vol(string):
    """Extracts the volume number from the information extracted from Zoobank

    Args:
        string (str): String being passed by the Item Pipeline

    Returns:
        str: String with the available volume
    """
    # Usually volume numbers immediatelly precedes '(' or ':'.
    # If, however, they are not present but we still have a number without '-'
    # or en-dash, this often means volume number
    # If none of these conditions are met, then, return empty string
    if '(' in string:
        return string[:string.find('(')]
    elif ':' in string:
        return string[:string.find(':')]
    elif '-' not in string and '–' not in string:
        return string
    else:
        return ''


def extract_issue(string):
    """Extracts the issue number from the information extracted from Zoobank

    Args:
        string (str): String being passed by the Item Pipeline

    Returns:
        str: String with the available issue
    """
    # This regex will get issue numbers, even if its separated by '-', en-dash,
    # or '/'.
    # Issues numbers are always presented in between parenteses, right after the
    # volume number
    issue = re.search('(?<=\()[0-9]+[\/|\-|\–]?[0-9]*(?=\))', string)

    # Thus, if there are the parentheses and a regex match, return it, otherwise
    # return an empty string
    if '(' in string and ')' in string and issue != None:
        return issue.group()
    else:
        return ''


def extract_start_page(string):
    """Extracts the start page from the information extracted from Zoobank.
    This is a very similar function to extract_end_page().

    Args:
        string (str): String being passed by the Item Pipeline

    Returns:
        str: String with the available start page
    """
    # This finds the ':' on the provided string, which is the bibliographic info
    # only, and start retrieving from there. This often works because page ran-
    # ges are provided after volume(issue), with a preceding ':' and a space.
    page_range = string[string.find(':'):].strip()

    # This regex recipe attempts to find any separator in the remaining string
    sep = re.search('[\-|\–]', page_range)

    # If there are the ':', and the separator actually found something, then
    # returns only the first of the two numbers available.
    if ':' in string and sep != None:
        return page_range[1:sep.start()].strip()

    # If there are the ':' but no separator, return the entire number.
    elif ':' in string:
        return string[string.find(':'):].strip()

    # If none of these were present, then return an empty string
    else:
        return ''


def extract_end_page(string):
    """Extracts the end page from the information extracted from Zoobank.
    This is a very similar function to extract_start_page().

    Args:
        string (str): String being passed by the Item Pipeline

    Returns:
        str: String with the available end page
    """
    # This finds the ':' on the provided string, which is the bibliographic info
    # only, and start retrieving from there. This often works because page ran-
    # ges are provided after volume(issue), with a preceding ':' and a space.
    page_range = string[string.find(':'):].strip()

    # This regex recipe attempts to find any separator in the remaining string
    sep = re.search('[\-|\–]', page_range)

    # If there are the ':', and the separator actually found something, then
    # returns only the second of the two numbers available.
    if ':' in string and sep != None:
        return page_range[sep.start() + 1:]

    # If the separator is not present, then return an empty string, because if
    # there is any number available, it's likely the start page.
    #TODO: This won't affect my analysis for the purpose of the Udacity's DSND
    # Capstone project, but I think I switch here: the remaining, isolated num-
    # ber should be end_page nor start_page as it's, currently. I have to think
    # more about this - and test it!
    else:
        return ''


class ZbItemLoader(ItemLoader):
    """Custom ItemLoader defined to simpligy the process of dealing with the
    information in the Item Pipeline

    Args:
        ItemLoader (Class): Inherits from scrapy.loader.ItemLoader
    """

    # Defines a default input processor. Basically, gets all parts of the resul-
    #ting string and combine them to be passed as one down the Item Pipeline
    #
    # To be honest, I should continue testing to see if I remove this will have
    # any affect on the out-processors. My guess is that it's not affecting it,
    # and problably because I haven't correctly declared this default_input_pro-
    # cessor
    default_input_processor = MapCompose(
        lambda x: "".join(x).replace('\n', '').replace('\t', '').replace('\r', ''),
        Join('')
    )

    # After joining the incoming pieces into a single string, this will select
    # all characters up until the pub. year (first occurence of 4 numbers)
    authors_out = Compose(
        lambda x: "".join(x),
        lambda x: x[:re.search('[0-9]{4}', x).start()].strip()
    )

    # This will join the incoming pieces, and retrieve the first occurence of
    # four numbers
    year_out = Compose(
        Join(''),
        lambda x: re.search('[0-9]{4}', x).group()
    )

    # After joining the incoming pieces, this regex recipe and string methods
    # will then get all remaining characters, spliting by period into a list,
    # and retrieving the first element, which shall contain the title
    title_out = Compose(
        Join(''),
        lambda x: x[re.search('[0-9]{4}', x).end():].strip().split('.')[0]
    )

    journal_out = Compose(
        Join(''),
        lambda x: x[re.search('[0-9]{4}', x).end():].strip().split('.')[1],
        lambda x: x[:re.search('[0-9]+', x).start()].strip() if re.search('[0-9]+', x) != None else x.strip()
    )

    # As the functions below became too complex, I couldn't use lambda in a
    # clear and intuitive way. Therefore, decided to declare regular functions.
    # The initial Join() has the same function described before - join pieces
    # to pass through the Item Pipeline
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

    # This is the simplest one: after adding the value directly from the spider,
    # this simply gets the first element on the provided list
    from_year_out = Compose(TakeFirst())