import pandas as pd

import etl.transform.doaj as doaj
import etl.transform.sherpa_romeo as sherpa

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
    4. Remove years out of the 2010-2020 range
    5. Select only 'journal' and 'year' columns
    6. Rename these two columns to 'Journal' and 'Year', with capitalization
    7. Add a column named 'Source', with all rows = 'Zoobank'

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
    ('Far Eastern Entomologist\(', 'Far Eastern Entomologist'),
    ('Insecta Mundi\(', 'Insecta Mundi'),
    ('Cesa News\(', 'Cesa News'),
    ('Zootaxa\,', 'Zootaxa'),
    ('Zootaxa\(', 'Zootaxa'),
    ('Centre for Entomological Studies, Miscellaneous Papers\(', 'Centre for Entomological Studies, Miscellaneous Papers'),
    ('European journal of taxonomy\(', 'European Journal of Taxonomy'),
    ('Ichthyological exploration of freshwaters\(IEF\-', 'Ichthyological Exploration of Freshwaters'),
    ('Journal of Melittology\(', 'Journal of Melittology'),
    ('Bulletin of the Mizunami Fossil Museum\(', 'Bulletin of the Mizunami Fossil Museum'),
    ('Revue suisse de zoologie', 'Revue suisse de Zoologie')
    ]

    for v1, v2 in values_and_replacement:
        zb['journal'] = zb['journal'].str.replace(v1, v2)

    # Removing higher ranked non-journals indexes
    zb = zb[zb['journal'] != ',']
    zb = zb[zb['journal'] != '']

    # Removing years out of the 2010-2020 range
    years_out = ['1847', '1877', '1878', '1880', '1881', '1883', '1887', '1888',
        '1889', '1894', '1896', '1898', '1902', '1905', '1917', '1919', '1923',
        '1927', '1932', '1933', '1936', '1937', '1951', '1952', '1960', '1962',
        '1967', '1969', '1972', '1986', '1989', '1996', '1999', '2001', '2002',
        '2003', '2004', '2008', '2009']

    for yr in years_out:
        zb = zb[zb['year'] != yr]

    # Selecting only the columns 'journal' and 'year'
    zb = zb[['journal', 'year']]

    # Renaming columns
    zb.rename(columns={'journal': 'Journal', 'year': 'Year'}, inplace=True)

    # Adding column 'Source', filling all rows = 'Zoobank'
    zb['Source'] = 'Zoobank'

    return zb


def combine(wos_final, tb_final, zb_final):
    """This function generates the final, combined dataframe that will be used
    to generate the charts and tables to answer the questions of this project.

    - It first selects the top 100 journals of each dataframe
    - Then concatenates them
    - Next, groups them by 'Journal', 'Source' and 'Year', and count
    their occurrences, unstacking 'Source' and 'Year' to became multindex
    columns.
    - Then, sort the columns indexes, to organize the year range
    - Finally, create sums per source
    - And a total sum that it's only used to...
    - ...sort the dataframe

    Args:
        wos_final (pandas.DataFrame): Transformed dataframe 1 (preferrably, wos)
        tb_final (pandas.DataFrame): Transformed dataframe 2 (preferrably, tb)
        zb_final (pandas.DataFrame): Transformed dataframe 3 (preferrably, zb)

    Returns:
        [type]: [description]
    """

    # Select all rows of the top 100 journals in each dataframe
    # First, get all top indexes
    wos_top_jrnl = wos_final.groupby('Journal')['Source'].count().sort_values(
        ascending=False).head(100).index

    tb_top_jrnl = tb_final.groupby('Journal')['Source'].count().sort_values(
        ascending=False).head(100).index

    zb_top_jrnl = zb_final.groupby('Journal')['Source'].count().sort_values(
        ascending=False).head(100).index

    # Then, slice the dataframes with those indexes
    wos = wos_final[wos_final['Journal'].isin(wos_top_jrnl)]

    tb = tb_final[tb_final['Journal'].isin(tb_top_jrnl)]

    zb = zb_final[zb_final['Journal'].isin(zb_top_jrnl)]

    # Concat all dataframes
    df = pd.concat([wos, tb, zb])

    # Group by 'Journal', 'Source' and 'Year' to create the desired multindex
    # dataframe with all counts
    df = df.groupby(['Journal', 'Source', 'Year'])['Journal'].count().unstack([
        'Source','Year'])

    # Sort multindex columns to organize year range from 2010 to 2020
    df = df.reindex(sorted(df.columns), axis=1)

    # Create all source-related sums
    yrs = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
        '2018', '2019', '2020']

    sources = ['TreatmentBank', 'Zoobank', 'WoS/Zoological Records']

    i = list()

    for s in sources:
        i = list()
        for y in yrs:
            i.append(df.columns.get_loc((s, y)))
            df[s, 'Sum'] = df.iloc[:, min(i):max(i)+1].sum(axis=1)

    # Create total sum by getting the index of the first sum column based on the
    # 'sources' list
    start_i = df.columns.get_loc((sources[0], 'Sum'))
    df['All', 'Sum'] = df.iloc[:, start_i:].sum(axis=1)

    # Sort it by the ('All', 'Sum')
    df.sort_values(by=[('All', 'Sum')], ascending=False, inplace=True)

    return df


def add_oa(df):
    """Adds a new column to the DF, based on the availability of information 
    regarding open-access status of the journals present in the dataframe, after
     calling both DOAJ and SHERPA/RoMEO.

    Args:
        df (pandas.DataFrame): Combined version of the dataframe

    Returns:
        pandas.DataFrame: Final.
    """

    journals = list(df.index)

    # Make DOAJ API call
    doaj_result = doaj.check_oa(journals)

    # Filter only the journals with None as result
    jrnls_after_doaj = [k for k in doaj_result if doaj_result[k] == None]

    # Call SHERPA/RoMEO
    sherpa_result = sherpa.check_oa(jrnls_after_doaj)

    # Join results
    jrnls_oa = doaj_result.copy()
    jrnls_oa.update(sherpa_result)

    # Creates a new column in df
    df[('All', 'OA')] = df.index.map(jrnls_oa)

    return df