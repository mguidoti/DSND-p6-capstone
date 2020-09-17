from os import path, listdir
import re
import pandas as pd


my_dir = './data/wos/'

my_files = [f for f in listdir(my_dir) if path.isfile(path.join(my_dir, f))]

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

    with open(filepath, mode='r', encoding="Utf-8") as input_file:

        record_list = list()
        record = dict()

        for line in input_file:

            if line[1:3] != 'FN' and line[:2] != 'VR':
                if line[:2] == 'ER':
                    record_list.append(record)
                    record = dict()
                elif re.search('[A-Z]+', line[:2]) != None:
                    cur = line[:2]
                    record[zr_fields.get(cur)] = line[3:].strip()
                elif line[:2] == "  ":
                    record[zr_fields.get(cur)] += ", " + line[3: ].strip()


    return record_list


def create_df(files_list):

    all_records = list()

    for file in files_list:
        all_records += zr_parser(path.join(my_dir, file))

    return pd.DataFrame(all_records)
