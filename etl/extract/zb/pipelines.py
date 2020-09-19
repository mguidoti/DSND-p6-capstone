# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from sqlalchemy.orm import sessionmaker

from zb.models import db_connect, create_table, Docs


class ZbPipeline:
    """This is a custom Item Pipeline class.
    """

    def __init__(self):
        """Init method, that instantiates an engine and create a table by
        calling zb.models.py methods, and start a Session.
        """

        engine = db_connect()
        create_table(engine)

        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Overwrited the process_item() required method for custom Item Proces-
        sors.

        Args:
            item (scrapy.Item): Item yield by the spider parser()
            spider (scrapy.Spider): Spider doing the crawling and passing the
            Items to be processed in this Pipeline

        Returns:
            [type]: [description]
        """

        session = self.Session()

        # Instantiates a Docs() object, to hold the information from the Item
        doc = Docs()

        doc.authors = item['authors']
        doc.year = item['year']
        doc.title = item['title']
        doc.journal = item['journal']
        doc.bibref_details = item['bibref_details']
        doc.volume = item['volume']
        doc.issue = item['issue']
        doc.start_page = item['start_page']
        doc.end_page = item['end_page']
        doc.from_year = item['from_year']

        # Attempt to add the Docs() object, and commit the changes on the data-
        #base
        try:
            session.add(doc)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        # Required return statement to pass the item to the remaining of the
        # pipeline (which in this case doesn't exist)
        return item
