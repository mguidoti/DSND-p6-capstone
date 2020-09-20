import requests

from etl.transform.config import SHERPA_KEY

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
        '5D&api-key={key}'.format(key=SHERPA_KEY, journal=titlecase(jrnl)))

        # Cold bloaded safety lock here. If requests fails, then, no value for
        # that specific journal
        try:
            r = requests.get(url)
            data = r.json()
        except:
            results[jrnl] = None

        try:
            info = data['items'][0]['publisher_policy']

            for each in info:

                oa = each['permitted_oa']

                for elem in oa:

                    if 'published' in elem['article_version']:

                        if elem['additional_oa_fee'] == 'yes':
                            results[jrnl] = 'Closed-access'
                        else:
                            results[jrnl] = 'GOLD|DIAMOND'
                    else:
                        pass
        except:
            results[jrnl] = None

    return results

def titlecase(journal):

    words = journal.split(' ')       # re.split behaves as expected
    final = [words[0].capitalize()]

    for word in words[1:]:

        final.append(word if word in
            ['of', 'the', 'to',
            'de', 'la', 'del', 'di',
            'for', 'and', 'in'] else word.capitalize())

    return " ".join(final)

#print(check_oa(['Zoological Journal of the Linnean Society']))         # Testing print

