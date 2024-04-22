import datetime
import os
import re


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

def keep_var(df, varlist: str | list, regularvars: str | list):
    if isinstance(varlist, str):
        return df[regularvars + [varlist]]
    elif isinstance(varlist, list):
        return df[regularvars + varlist]
    else:
        raise ValueError('Only accept one variable name (string) or a list of variable names.')