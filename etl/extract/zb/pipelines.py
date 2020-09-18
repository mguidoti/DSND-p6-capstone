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

    def __init__(self):

        engine = db_connect()
        create_table(engine)

        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):

        session = self.Session()

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

        try:
            session.add(doc)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
