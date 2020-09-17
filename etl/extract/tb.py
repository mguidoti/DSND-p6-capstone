import requests
import pandas as pd

def get_data():

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
        return "Something went wrong. Status code: {}. Reason: {}".format(
            r.status_code,
            r.reason)

def create_df(data):

    if type(data) is str:
        return data

    else:
        df = pd.DataFrame(data)

        df.drop(['DocArticleUuid', 'TreatStatus'], axis=1, inplace=True)

        df.rename(columns={'DocCount': 'Docs', 'BibYear': 'Year', 'BibSource': 'Journal', 'ContTreatCount': 'Treatments'}, inplace=True)

        df = df[['Journal', 'Year', 'Docs', 'Treatments']]

        return df
