import pandas as pd

def wos(wos):
    """[summary]

    Args:
        wos ([type]): [description]
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
    """[summary]

    Args:
        tb ([type]): [description]
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
    """[summary]

    Args:
        zb ([type]): [description]
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
        'Bulletin of the Mizunami Fossil Museum\('
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



