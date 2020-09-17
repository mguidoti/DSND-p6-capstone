import requests
import pandas as pd

def get_data():
    """Retrieve TreatmentBank (Plazi) data from a pre-determine API call

    Raises:
        TypeError: If we got anything else but a 200, this exception will be
        raised as we won't be able to build a pandas.DataFrame from the response

    Returns:
        dict: A dictionary containing the data from TreatmentBank API
    """

    r = requests.get('http://tb.plazi.org/GgServer/dioStats/stats?outputFields='
        'doc.articleUuid+bib.year+bib.source+cont.treatCount+treat.status&'
        'groupingFields=bib.year+bib.source&orderingFields=doc.articleUuid&'
        'FP-bib.year=2010-2020&FP-treat.status=%22sp.%20nov.%22%20%22NEW%20'
        'SSP.%22%20%22SP.%20NOV.%22%20%22nov.sp.%22%20%22Spec.%20Nov.%22%20'
        '%22N.SP.%22%20%22Sp.%20nov.%22%20%22NEW%20SP.%22%20%22nov.%20spec.'
        '%22%20%22sp%20nov.%22%20%22New%20SpecIes%22&FA-cont.treatCount=count&'
        'format=JSON')


    if r.status_code == 200:

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