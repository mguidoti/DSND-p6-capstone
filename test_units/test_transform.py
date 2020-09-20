import pandas as pd

def wos(wos):
    """Test unit for data transformation of Web of Science/Zoological Records 
    dataframe

    Args:
        wos (pandas.DataFrame): Web of Science/Zoological Records dataframe
    """

    # Check if the columns were correctly set
    try:
        assert(set(wos.columns) == set(['Journal', 'Year', 'Source']))
        print("SUCCESS! You correctly selected the columns!")
    except:
        print("FAILED! Your wos dataframe has different collumns "
            "than expected.")

    # Check if the value in 'Source' is correct
    try:
        assert(wos['Source'].unique()[0] == 'WoS/Zoological Records')
        print("SUCCESS! You correctly filled the collumn 'Source'!")
    except:
        print("FAILED! Your wos dataframe has different values in column "
            "'Source' than expected.")


def tb(tb):
    """Test unit for data transformation of TreatmentBank dataframe

    Args:
        tb (pandas.DataFrame): TreatmentBank dataframe
    """

    # Check if the columns were correctly set
    try:
        assert(set(tb.columns) == set(['Journal', 'Year', 'Source']))
        print("SUCCESS! You correctly selected the columns!")
    except:
        print("FAILED! Your tb dataframe has different collumns "
            "than expected.")

    # Check if the value in 'Source' is correct
    try:
        assert(tb['Source'].unique()[0] == 'TreatmentBank')
        print("SUCCESS! You correctly filled the collumn 'Source'!")
    except:
        print("FAILED! Your tb dataframe has different values in column "
            "'Source' than expected.")


def zb(zb):
    """Test unit for data transformation of Zoobank dataframe

    Args:
        zb (pandas.DataFrame): Zoobank dataframe
    """

    # Check if high-ranked journals wrongly named were renamed
    undesired_values = [
        'Insecta mundi',
        'Peckhamia\(',
        'ZooKeys\(',
        'European Journal of Taxonomy\(',
        'Far Eastern Entomologist\(',
        'Insecta Mundi\(',
        'Cesa News\(',
        'Zootaxa\,',
        'Zootaxa\(',
        'Centre for Entomological Studies, Miscellaneous Papers\(',
        'European journal of taxonomy\(',
        'Ichthyological exploration of freshwaters\(IEF\-',
        'Journal of Melittology\(',
        'Bulletin of the Mizunami Fossil Museum\(',
        'Revue suisse de zoologie'
    ]

    # Bool that will be used in the assert
    passed = True

    # Iterates over the list, checking the presence of each value on the df
    for value in undesired_values:
        if len(zb[zb['Journal'] == value]) > 0:
            passed = False
        else:
            # Removes the word that wasn't found
            undesired_values.remove(value)

    try:
        assert(passed == True)
        print("SUCCESS! You correctly fixed all pre-determined values!")
    except:
        print("FAILED! The following undesirable values are still on the "
            "zb dataframe: {}".format(undesired_values))

    # Check if rows with 'journal' equals to "", and "," were removed
    undesired_values = ['', ',']

    # Bool that will be used in the assert
    passed = True

    # Iterates over the list, checking the presence of each value on the df
    for value in undesired_values:
        if len(zb[zb['Journal'] == value]) > 0:
            passed = False
        else:
            # Removes the word that wasn't found
            undesired_values.remove(value)

    try:
        assert(passed == True)
        print("SUCCESS! You correctly removed '' and ','!")
    except:
        print("FAILED! The following undesirable values are still on the "
            "zb dataframe: {}".format(undesired_values))

    # Check if all out of range years were correctly removed
    years_out = ['1847', '1877', '1878', '1880', '1881', '1883', '1887', '1888',
        '1889', '1894', '1896', '1898', '1902', '1905', '1917', '1919', '1923',
        '1927', '1932', '1933', '1936', '1937', '1951', '1952', '1960', '1962',
        '1967', '1969', '1972', '1986', '1989', '1996', '1999', '2001', '2002',
        '2003', '2004', '2008', '2009']

    # Bool that will be used in the assert
    passed = True

    # Iterates over the list, checking the presence of each value on the df
    for yr in years_out:
        if len(zb[zb['Year'] == yr]) > 0:
            passed = False
        else:
            # Removes the word that wasn't found
            years_out.remove(yr)

    try:
        assert(passed == True)
        print("SUCCESS! You correctly removed all years out of the 2010-2020 "
            "range!")
    except:
        print("FAILED! The following out of range years are still on your "
            "dataframe: {}".format(years_out))

    # Check if the columns were correctly set
    try:
        assert(set(zb.columns) == set(['Journal', 'Year', 'Source']))
        print("SUCCESS! You correctly selected the columns!")
    except:
        print("FAILED! Your zb dataframe has different collumns "
            "than expected.")

    # Check if the value in 'Source' is correct
    try:
        assert(zb['Source'].unique()[0] == 'Zoobank')
        print("SUCCESS! You correctly filled the collumn 'Source'!")
    except:
        print("FAILED! Your zb dataframe has different values in column "
            "'Source' than expected.")


def final(df):
    """Test if the combination of all transformed dataframes was successfull.

    Args:
        df (pandas.DataFrame): Final, transformed and combined dataframe
    """

    # Checks if the each source Sum column was correctly created

    # Bool that will be used in the assert
    passed = True

    sources = ['TreatmentBank', 'Zoobank', 'WoS/Zoological Records']

    for s in sources:
        try:
            df[(s, 'Sum')]
            sources.remove(s)
        except:
            passed = False

    try:
        assert(passed)
        print("SUCCESS! You successfully created the Sources-specific "
            "Sum columns!")
    except:
        print("FAILED! Apparently, there is no Sum column "
            "for {}".format(sources))

    # Checks if ('All', 'Sum' was correctly created)
    try:
        assert(type(df[('All', 'Sum')]) == pd.core.series.Series)
        print("SUCCESS! The ('All', 'Sum') function was correctly set!")
    except:
        print("FAILED! There is no ('All', 'Sum') function.")

    # Checks if the datafrase was correctly sorted by trying to retrieve what
    # should be journal #8 and journal #24
    passed = True

    if df.iloc[7,:].name != 'Acta Entomologica Musei Nationalis Pragae':
        passed = False
    elif df.iloc[23,:].name != 'PeerJ':
        passed = False

    try:
        assert(passed)
        print("SUCCESS! The final dataframe seems to be correctly sorted!")
    except:
        print("FAILED! The final dataframe is not sorted as supposed to.")