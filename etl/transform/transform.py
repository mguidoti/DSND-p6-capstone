import pandas as pd

def wos(wos):
    """Transform the wos dataset according to what was found in the explaratory
    analyses, available on sp_np.ipynb

    1. Remove duplicates based on columns: 'Source', 'Year Published', 'Volume',
    'Issue', 'Page Span' columns;
    2. Select only 'Source' and 'Year Published' columns
    3. Rename these two columns to 'Journal' and 'Year'
    4. Add a column named 'Source', with all rows = 'WoS/Zoological Records'

    Args:
        wos (pandas.DataFrame): Unchanged dataframe from the Web of Science/Zoo-
        logical records parser

    Returns:
        pandas.DataFrame: Transformed wos dataframe
    """
    # Removing duplicates
    wos.drop_duplicates(subset=['Source', 'Year Published', 'Volume',
        'Issue', 'Page Span'], keep=False, inplace=True)

    # Selecting only the columns 'Source' and 'Year Published'
    wos = wos[['Source', 'Year Published']]

    # Renaming columns
    wos.rename(columns={'Source': 'Journal', 'Year Published': 'Year'},
        inplace=True)

    # Adding column 'Source', filling all rows = 'WoS/Zoological Records'
    wos['Source'] = 'WoS/Zoological Records'

    return wos


def tb(tb):
    """Transform the tb dataset according to what was found in the explaratory
    analyses, available on sp_np.ipynb

    1. Select only 'journal' and 'year' columns
    2. Rename these two columns to 'Journal' and 'Year', with capitalization
    3. Add a column named 'Source', with all rows = 'TreatmentBank'

    Args:
        tb (pandas.DataFrame): Unchanged dataframe from TreatmentBank processor

    Returns:
        pandas.DataFrame: Transformed tb dataframe
    """
    # Selecting only the columns 'journal' and 'year'
    tb = tb[['journal', 'year']]

    # Renaming columns
    tb.rename(columns={'journal': 'Journal', 'year': 'Year'}, inplace=True)

    # Adding column 'Source', filling all rows = 'TreatmentBank'
    tb['Source'] = 'TreatmentBank'

    return tb


def zb(zb):
    """Transform the zb dataset according to what was found in the explaratory
    analyses, available on sp_np.ipynb

    1. Remove duplicates based on 'journal' and 'bibref_details' columns
    2. Rename some high-ranked journals
    3. Remove rows that contains higher ranked non-jounals, such as "nov",
    "n", etc.
    4. Select only 'journal' and 'year' columns
    5. Rename these two columns to 'Journal' and 'Year', with capitalization
    6. Add a column named 'Source', with all rows = 'Zoobank'

    Args:
        zb (pandas.DataFrame): Unchanged dataframe from Zoobank scraper

    Returns:
        pandas.DataFrame: Transformed zb dataframe
    """
    # Removing duplicates
    zb.drop_duplicates(subset=['journal', 'bibref_details'], keep=False,
        inplace=True)

    # Renaming some high-ranked journals
    values_and_replacement = [
    ('Insecta mundi', 'Insecta Mundi'),
    ('Peckhamia\(', 'Peckhamia'),
    ('ZooKeys\(', 'ZooKeys'),
    ('European Journal of Taxonomy\(', 'European Journal of Taxonomy'),
    ('Far Eastern Entomologist\(', ''),
    ('Insecta Mundi\(', 'Insecta Mundi'),
    ('Cesa News\(', 'Cesa News'),
    ('Zootaxa\,', 'Zootaxa'),
    ('Zootaxa\(', 'Zootaxa'),
    ('Centre for Entomological Studies, Miscellaneous Papers\(', 'Centre for Entomological Studies, Miscellaneous Papers'),
    ('European journal of taxonomy\(', 'European Journal of Taxonomy'),
    ('Ichthyological exploration of freshwaters\(IEF\-', 'Ichthyological Exploration of Freshwaters'),
    ('Journal of Melittology\(', 'Journal of Melittology'),
    ('Bulletin of the Mizunami Fossil Museum\(', 'Bulletin of the Mizunami Fossil Museum')
    ]

    for v1, v2 in values_and_replacement:
        zb['journal'] = zb['journal'].str.replace(v1, v2)

    # Removing higher ranked non-journals indexes
    zb = zb[zb['journal'] != ',']
    zb = zb[zb['journal'] != '']



    # Selecting only the columns 'journal' and 'year'
    zb = zb[['journal', 'year']]

    # Renaming columns
    zb.rename(columns={'journal': 'Journal', 'year': 'Year'}, inplace=True)

    # Adding column 'Source', filling all rows = 'Zoobank'
    zb['Source'] = 'Zoobank'

    return zb


def combine(wos, tb, zb):

    # Select top 100
    # testing = zbt.groupby('journal').count()['year'].sort_values(ascending=False).head(60)

    # Pre combining routine
    '''
    tb3 = tb2.groupby(['Journal', 'Source', 'Year'])['Journal'].count().unstack(['Source','Year'])
    tb3 = tb3.reindex(sorted(tb3.columns), axis=1)
    tb3['TreatmentBank', 'final'] = tb3.iloc[:, 0:].sum(axis=1)
    tb3.sort_values(by=[('TreatmentBank', 'final')], ascending=False)
    '''


    return df


def add_oa(df):

    return df