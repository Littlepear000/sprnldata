
import pandas as pd
import os
import re
import datetime
from sprnldata.myclass.base import ImfFrame
from sprnldata.downloads.ecos.ecosset import folder_ecos


def get_latest_file(folder_path):
    files = os.listdir(folder_path)
    timelist = []
    for file in files:
        if file.endswith('.csv'):
            timestamp = datetime.datetime.strptime(re.findall(r'\d{8}', file)[0], '%Y%m%d')
            timelist.append(timestamp)
    max_time = max(timelist).strftime('%Y%m%d')
    return max_time


class EcosData(ImfFrame):
    def __init__(self,
                 *args,
                 version='latest',
                 **kwargs
    ):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            local_version = get_latest_file(folder_ecos) if version == 'latest' else version
            raw = pd.read_csv(f'{folder_ecos}/ecosdata_{local_version}.csv')
            super().__init__(raw)

    def keep_var(self, varlist: str | list):
        regularvars = ['ifscode', 'year']
        if isinstance(varlist, str):
            finalvars = regularvars + [varlist]
        else:
            finalvars = regularvars + varlist
        df = self[finalvars]
        return df


if __name__ == '__main__':
    a = EcosData(version='latest')
    b = a.df
    c = a.keep_var(['ngdpd', 'pfb_gdp'])