import datetime
import os
import re
import pandas as pd

countrycode_file = r'Q:\DATA\SPRNL\Users\NL RA\Country Code & Template\Country Code & Grouping\Country Codes.xlsx'
countrycode = pd.read_excel(countrycode_file, sheet_name='Match')

countryname_to_ifs = {row['Name']: int(row['Code']) for index, row in countrycode.iterrows()}
countryname_to_iso = {row['Name']: row['ISO-3 code'] for index, row in countrycode.iterrows()}
ifs_to_iso = {int(row['Code']): row['ISO-3 code'] for index, row in countrycode.iterrows()}


def get_latest_file(folder_path, debug=False):
    files = os.listdir(folder_path)
    if debug:
        print(files)
    timelist = []
    for file in files:
        if file.endswith('.csv') or file.endswith('.xlsx'):
            timestamp = datetime.datetime.strptime(re.findall(r'\d{8}', file)[0], '%Y%m%d')
            timelist.append(timestamp)
    max_time = max(timelist).strftime('%Y%m%d')
    return max_time
