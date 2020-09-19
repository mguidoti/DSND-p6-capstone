from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text, Integer


Base = declarative_base()


def db_connect():
    """Establishes a connection with the SQLite database

    Returns:
        Engine: Engine used to power up the connection with a database
    """
    return create_engine('sqlite:///data/tb.db')


def create_table(engine):
    """Creates a table in the database, if it doesn't exist

    Args:
        engine (Engine): Engine used to power up the connection with a database
    """
    Base.metadata.create_all(engine)


class Docs(Base):
    """Used to hold the different records being retrieved from TreatmentBank

    Args:
        Base (Class): Inherits from class Base, the base class which all mapped
        classes should inherit
        inherit
    """
    # Declare table name
    __tablename__ = "docs"

    # Columns and their types
    id = Column(Integer, primary_key=True)
    authors = Column('authors', Text())
    year = Column('year', Text())
    title = Column('title', Text())
    journal = Column('journal', Text())
    volume = Column('volume', Text())
    issue = Column('issue', Text())
    start_page = Column('start_page', Text())
    end_page = Column('end_page', Text())
    number_of_treatments = Column('num_treats', Text())
