import pandas as pd
import xlwings as xw
import re
from sprnldata.core.mona.config import *
from sprnldata.core.mona.data import MonaData, getlatestv
import sprnldata.core.dummy.config as dum
from sprnldata.downloads.ecos.ecosset import EcosData


def _dbengine(version):
    if version == 'latest':
        filename = getlatestv(tab='d')
    else:
        filename = f'{monatab["d"]}_{version}.xlsx'

    raw = pd.read_excel(f'{dbpath}/{filename}')
    raw['Review Sequence'] = raw['Review Sequence'].apply(lambda x: x.strip())
    raw['Account'] = raw['Arrangement Type'].apply(lambda x: account_match(x) if x.find('-') < 0 else 'PRGT')
    raw['Actual End Date'] = raw.apply(
        lambda row: row['Initial End date'] if pd.isna(row['Revised End Date']) else row['Revised End Date'], axis=1)
    raw['Actual End Year'] = raw['Actual End Date'].dt.year
    raw['T'] = raw.apply(
        lambda row: row['Approval Year'] + 1 if row['Approval Date'].quarter == 4 else row['Approval Year'], axis=1)
    raw = raw[raw['Review Sequence'].isin(['L', 'EL', 'REL'])][list(col_des.keys())].rename(
        columns=col_des)  # keep lastest
    raw['country'] = raw['country'].apply(lambda x: x.title())
    return raw

def account_match(value):
    for key, values_list in account_map.items():
        if value in values_list:
            return key
    return None

def expand_rows(row, start: str = 'start', end: str = 'end', on: str = 'T'):
    pattern = '([Tt]\s*[+-]\s*\d)'

    if start == 'start':
        m = 0
    elif re.match(pattern, start):
        m = int(re.findall('[+-]\s*\d', start)[0].replace(' ', ''))
    else:
        raise ValueError('Check start value: only accept "start" or "T+(number)/T-(number)" format')

    if end == 'end':
        n = row['end_year'] - row['app_year']
    elif re.match(pattern, end):
        n = int(re.findall('[+-]\s*\d', end)[0].replace(' ', ''))
    else:
        raise ValueError('Check end value: only accept "end" or "T+(number)/T-(number)" format')

    if on in ['T', 'app_year']:
        benchmark = row['app_year'] if on == 'app_year' else row['T']
        new_rows = []
        for year in range(m, n + 1):
            new_rows.append({
                'arrnum': row['arrnum'],
                'ifscode': row['ifscode'],
                'account': row['account'],
                'start_date': row['app_date'],
                'end_date': row['end_date'],
                'T': row['T'],
                'year': benchmark + year,
                'year_label': 'T' if year == 0 else f'T+{str(year)}' if year>0 else f'T{str(year)}'} )
    else:
        raise ValueError('Parameter "on" only accept "T" or "app_year"')
    return pd.DataFrame(new_rows)


class MonaDes(MonaData):
    def __init__(self, *args, version='latest', **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            df = _dbengine(
                version=version
            )
            super().__init__(df)
        self.dbtype = 'd'

    @property
    def roc2018(self):
        return self.loc[self['roc2018'] == 1]

    @property
    def roc2025(self):
        return self.loc[self['roc2025'] == 1]

    def get_weo(
            self,
            varlist: list,
            dbname: str = 'WEO_WEO_PUBLISHED'
    ):
        # Under Mona cir, only Annual Freq data requested
        # ... and always pull all countries
        pull_dict = {
            'Database 1': {
                'dbname': dbname,
                'indlist': varlist,
                'clist': list(self['ifscode'].unique()),
                'freq': 'A'
            }
        }
        weo = EcosData(pull_dict=pull_dict).rename(columns={'year':'T'})
        df = pd.merge(self, weo, on=['ifscode', 'T'], how='left')
        return df

    def get_weo_from_file(
            self,
            filename: str,
            sheetname: str =None
    ):
        sheetname = xw.Book(filename).sheets[0].name if not sheetname else sheetname
        weo = pd.read_excel(filename, sheetname)
        if 'ifscode' in weo.columns and 'year' in weo.columns:
            weo.rename(columns={'year': 'T'}, inplace='True')
            df = pd.merge(self, weo, on=['ifscode', 'T'], how='left')
        else:
            print('Must have ifscode and year')
            df = None
        return df

    def expand(self, start: str = 'start', end: str = 'end', on: str = 'T'):
        df = pd.concat([expand_rows(row, start=start, end=end, on=on) for _, row in self.iterrows()], ignore_index=True)
        return MonaDes(df)

    @property
    def _constructor(self):
        return MonaDes


if __name__ == '__main__':
    a = MonaDes()
    # b = a.get_weo(['NGDP', 'NGDPD'])
    # c = b.get_weo(['GGR'], dbname='WEO_WEO_LIVE')
    d = a.expand(start='T-5', end='T+5')
