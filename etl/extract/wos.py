from os import path, listdir
import re
import pandas as pd


my_dir = './data/wos/'      # Define folder where the output files are kept

# List all files in the specified folder
my_files = [f for f in listdir(my_dir) if path.isfile(path.join(my_dir, f))]

# Data dictionary based on Zoological Records documentation, used to translate
# the output fields into meaningful columns. Link:
# https://images.webofknowledge.com/images/help/ZOOREC/hs_zoorec_fieldtags.html
zr_fields = {
    'FN': 'File Name',
    'VR': 'Version Number',
    'PT': 'Publication Type',
    'AN': 'Zoological Record Accession Number',
    'DT': 'Document Type',
    'TI': 'Title',
    'FT': 'Foreign Title',
    'AU': 'Authors',
    'BA': 'Book Authors',
    'GP': 'Group Authors',
    'ED': 'Editors',
    'SO': 'Source',
    'VL': 'Volume',
    'IS': 'Issue',
    'SU': 'Supplement',
    'PS': 'Page Span',
    'PD': 'Publication Date',
    'PY': 'Year Published',
    'UR': 'Journal URL',
    'AW': 'Item URL',
    'NT': 'Notes',
    'LA': 'Language',
    'AB': 'Abstract',
    'C1': 'Author Address',
    'EM': 'E-mail Address',
    'RI': 'ResearcherID Number',
    'OI': 'ORCID Identifier (Open Researcher and Contributor ID)',
    'U1': 'Usage Count (Last 180 Days)',
    'U2': 'Usage Count (Since 2013)',
    'PU': 'Publisher',
    'PA': 'Publisher Address',
    'SC': 'Research Areas',
    'SN': 'International Standard Serial Number (ISSN)',
    'BN': 'International Standard Book Number (ISBN)',
    'BD': 'Broad Terms',
    'DE': 'Descriptors Data',
    'TN': 'Taxa Notes',
    'ST': 'Super Taxa',
    'OR': 'Systematics',
    'DI': 'Digital Object Identifier (DOI)',
    'UT': 'Unique Article Identifier',
    'OA': 'Open Access Indicator',
    'HP': 'ESI Hot Paper. Note that this field is valued only for ESI subscribers',
    'HC': 'ESI Highly Cited Paper. Note that this field is valued only for ESI subscribers',
    'DA': 'Date this report was generated',
    'ER': '[End of Record]',
    'EF': '[End of File]',
}

def zr_parser(filepath):
    """Parse the plain text output format from Clarivate's Zoological Record

    Args:
        filepath (str): String with the filepath to the Zoological Record's
        output file.

    Returns:
        list: List of dictionaries, each dictionary containing one record from
        Zoological Record's output files.
    """

    with open(filepath, mode='r', encoding="Utf-8") as input_file:

        record_list = list()
        record = dict()

        for line in input_file:
            # Avoid the first two lines of the file
            if line[1:3] != 'FN' and line[:2] != 'VR':
                # If the line means 'End of Record', then add the dict to the
                # list, and renew the dict
                if line[:2] == 'ER':
                    record_list.append(record)
                    record = dict()
                # Search for lines that start with a field. If so, create the
                # key on the current dictionary
                elif re.search('[A-Z]+', line[:2]) != None:
                    cur = line[:2]
                    record[zr_fields.get(cur)] = line[3:].strip()
                # If not, check if there are two spaces at the beginning. These
                # are associated with multi-value fields, like Authors. Plus,
                # the lines in between records are singled spaced, which means,
                # this also avoids them.
                elif line[:2] == "  ":
                    record[zr_fields.get(cur)] += ", " + line[3: ].strip()

    return record_list


def create_df(files_list):
    """Return a Pandas DataFrame from Zoological Record's output file(s).

    Args:
        files_list (list): List with the output file names to be processed.

    Returns:
        pandas.DataFrame: DataFrame with all data, saved in different files, combined.
    """

    all_records = list()

    for file in files_list:
        all_records += zr_parser(path.join(my_dir, file))

    return pd.DataFrame(all_records)
