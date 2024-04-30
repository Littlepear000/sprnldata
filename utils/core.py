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
