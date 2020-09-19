import requests
import pickle
import pandas as pd

from sqlalchemy.orm import sessionmaker

from etl.extract.tb_model import db_connect, create_table, Docs


def get_data():
    """Retrieve TreatmentBank (Plazi) data from a pre-determine API call

    Raises:
        TypeError: If we got anything else but a 200, this exception will be
        raised as we won't be able to build a pandas.DataFrame from the response

    Returns:
        dict: A dictionary containing the data from TreatmentBank API
    """

    # Pre-defined API call
    r = requests.get('http://tb.plazi.org/GgServer/dioStats/stats?outputFields='
        'doc.articleUuid+bib.author+bib.title+bib.year+bib.source+bib.volume+'
        'bib.issue+bib.numero+bib.firstPage+bib.lastPage+cont.treatCount+treat.'
        'status&groupingFields=bib.author+bib.title+bib.year+bib.source+bib.'
        'volume+bib.issue+bib.numero+bib.firstPage+bib.lastPage&orderingFields='
        'doc.articleUuid&FP-bib.year=2010-2020&FP-treat.status=%22sp.%20nov.%22'
        '%20%22NEW%20SSP.%22%20%22SP.%20NOV.%22%20%22nov.sp.%22%20%22Spec.%20'
        'Nov.%22%20%22N.SP.%22%20%22Sp.%20nov.%22%20%22NEW%20SP.%22%20%22nov.'
        '%20spec.%22%20%22sp%20nov.%22%20%22New%20SpecIes%22&FA-cont.'
        'treatCount=count&format=JSON')

    if r.status_code == 200:

        # Save the full response to test the data consistency with the .db
        # later
        with open('./data/tb_response.p', 'wb') as p_file:
            pickle.dump(r.json(), p_file)

        return r.json()['data']

    else:
        raise TypeError('Something went wrong. Status code: {}, reason: {}'
            .format(r.status_code, r.reason))


def create_df():
    """Creates a pandas.DataFrame out of the data retrieved from TreatmentBank

    Returns:
        pandas.DataFrame: Dataframe contaning all information retrieved
    """

    data = get_data()

    return pd.DataFrame(data)


def create_db(data):
    """Creates a SQLite database with the processed data received from Treatment
    bank

    Args:
        data (dict): Data from TreatmentBank
    """

    # Create engine and establish a session with db
    engine = db_connect()
    create_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    count = 0

    for entry in data:

        doc = Docs()

        doc.authors = entry['BibAuthor']
        doc.year = entry['BibYear']
        doc.title = entry['BibTitle']
        doc.journal = entry['BibSource']
        doc.volume = entry['BibVolume']
        doc.issue = entry['BibIssue']
        doc.start_page = entry['BibFirstPage']
        doc.end_page = entry['BibLastPage']
        doc.number_of_treatments = entry['ContTreatCount']

        try:
            session.add(doc)
        except:
            session.rollback()
            raise

        count += 1

    # Commit additions and close session
    session.commit()
    session.close()

    # Print general status on terminal
    print("A total of {} records were processed.".format(count))