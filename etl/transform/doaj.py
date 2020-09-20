import requests

# List of journals used to test the function
'''
journals = [
    'Zootaxa',
    'ZooKeys',
    'European Journal of Taxonomy',
    'Iheringia: Série Zoologia',
    'Check List',
    'Revista Nicaraguense de Entomologia'
    ]
'''

def check_oa(jrnls_list):

    jrnls_list = [j.replace(':', '') for j in jrnls_list]

    results = dict()

    for jrnl in jrnls_list:


        url = ('https://doaj.org/api/v1/search/journals/{}'
            .format(jrnl))

        # Cold bloaded safety lock here. If requests fails, then, no value for
        # that specific journal
        try:
            r = requests.get(url)
            data = r.json()
        except:
            results[jrnl] = None

        if data['total'] == 0:
            results[jrnl] = None
        else:
            # TODO: Can and SHOULD improve this title comparison to accomodate
            # differne tittle cases and additional words, such as, publishers.
            if data['results'][0]['bibjson']['title'] == jrnl:
                try:
                    oa_apc = data['results'][0]['bibjson']['apc']
                    results[jrnl] = 'GOLD'
                except:
                    results[jrnl] = 'DIAMOND'
            else:
                results[jrnl] = None

    return results

# print(check_oa(journals))         # Testing print


