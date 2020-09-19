import requests

from config import SHERPA_KEY

# List of journals used to test the function
'''
journals = [
    'Zootaxa',
    'ZooKeys',
    'European Journal of Taxonomy',
    'Iheríngia',
    'Check List',
    'Revista Nicaraguense de Entomologia',
    'Phytotaxa',
    'Zoological Journal of the Linnean Society',
    'Zoologia'
    ]
'''

def check_oa(jrnls_list):

    results = dict()

    for jrnl in jrnls_list:

        url = ('https://v2.sherpa.ac.uk/cgi/retrieve?item-type=publication&format=Json&'
        'limit=10&filter=%5B%5B%22title%22%2C%22equals%22%2C%20%22{journal}%22%5D%'
        '5D&api-key={key}'.format(key=SHERPA_KEY, journal=jrnl))

        r = requests.get(url)
        data = r.json()

        try:
            info = data['items'][0]['publisher_policy'][0]['permitted_oa']

            for each in info:

                if 'published' in each['article_version']:

                    if each['additional_oa_fee'] == 'yes':
                        results[jrnl] = 'Closed-access'
                    else:
                        results[jrnl] = 'GOLD|DIAMOND'
                else:
                    pass
        except:
            results[jrnl] = None

    return results

# print(check_oa(journals))         # Testing print