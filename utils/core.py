import datetime
import os
import re
import pandas as pd
from sprnldata.config import onedrive_root

countrycode_file = fr'{onedrive_root}\0_tools\Country Code & Template\Country Code & Grouping\Country Codes.xlsx'
countrycode = pd.read_excel(countrycode_file, sheet_name='Match')
countrycode.loc[countrycode['Code'] == 728, 'ISO-2 code'] = 'NA'

countryname_to_ifs = {row['Name']: int(row['Code']) for index, row in countrycode.iterrows()}
countryname_to_iso = {row['Name']: row['ISO-3 code'] for index, row in countrycode.iterrows()}
countryname_to_iso2 = {row['Name']: row['ISO-2 code'] for index, row in countrycode.iterrows()}
ifs_to_iso = {int(row['Code']): row['ISO-3 code'] for index, row in countrycode.iterrows()}
iso_to_ifs = {row['ISO-3 code']: int(row['Code']) for index, row in countrycode.iterrows() if row['ISO-3 code'] is not None}
iso2_to_ifs = {row['ISO-2 code']: int(row['Code']) for index, row in countrycode.iterrows() if row['ISO-2 code'] is not None}
ifs_to_countryname = {int(row['Code']): row['Name'] for index, row in countrycode.iterrows()}
iso_to_countryname = {row['ISO-3 code']: row['Name'] for index, row in countrycode.iterrows()}
iso2_to_countryname = {row['ISO-2 code']: row['Name'] for index, row in countrycode.iterrows()}

def get_latest_file(folder_path, debug=False):
    files = os.listdir(folder_path)
    if debug:
        print(files)
    timelist = []
    # print(files)
    for file in files:
        if file.endswith('.csv') or file.endswith('.xlsx'):
            if re.search(r'\d{8}', file):
                timestamp = datetime.datetime.strptime(re.findall(r'\d{8}', file)[0], '%Y%m%d')
                timelist.append(timestamp)
    max_time = max(timelist).strftime('%Y%m%d')
    return max_time
