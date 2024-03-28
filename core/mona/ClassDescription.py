import pandas as pd
import pandaspro as cpd
import imf_datatools
import xlwings as xw
import re
from sprnldata.core.mona.config import *
from sprnldata.core.mona.data import MonaData, getlatestv
from sprnldata.core.dummy.config import roc2018raw, roc2025raw
from sprnldata.core.ecos.data import EcosData

def account_match(value):
    for key, values_list in account_map.items():
        if value in values_list:
            return key
    return None

def prog_dummy(df):
    roc_dfs = {'2018': roc2018raw, '2025': roc2025raw}
    for year, roc_df in roc_dfs.items():
        new_column_name = f'roc{year}'
        roc_df.rename(columns={'Arrangement Number': 'arrnum'}, inplace=True)
        roc_df[new_column_name] = 1
        df = pd.merge(df, roc_df[['arrnum', new_column_name]], on='arrnum', how='left')
        df[new_column_name] = df[new_column_name].fillna(0)
    return df

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
                'end_date': row['end_date'],
                'year': benchmark + year,
                'year_label': 'T' if year == 0 else f'T+{str(year)}' if year>0 else f'T{str(year)}'} )
    else:
        raise ValueError('Parameter "on" only accept "T" or "app_year"')
    return pd.DataFrame(new_rows)

# 1. df.get_weo(varlist)
# 2. df.get_vintage(varlist)
# 3. df.expand(from, to)

class MonaDes(MonaData):
    def __init__(self, *args, version='latest', **kwargs):
        dbtype = 'd'
        check = MonaData(*args, **kwargs).empty
        if not check:
            super().__init__(*args, **kwargs)
        else:
            if version == 'latest':
                filename = getlatestv(tab=dbtype)
            else:
                filename = f'{monatab[dbtype]}_{version}.xlsx'

            raw = pd.read_excel(f'{dbpath}/{filename}')
            raw['Review Sequence'] = raw['Review Sequence'].apply(lambda x: x.strip())
            raw['Account'] = raw['Arrangement Type'].apply(lambda x: account_match(x) if x.find('-') < 0 else 'PRGT')
            raw['Actual End Date'] = raw.apply(
                lambda row: row['Initial End date'] if pd.isna(row['Revised End Date']) else row['Revised End Date'], axis=1)
            raw['Actual End Year'] = raw['Actual End Date'].dt.year
            raw['T'] = raw.apply(
                lambda row: row['Approval Year'] + 1 if row['Approval Date'].quarter == 4 else row['Approval Year'], axis=1)
            raw = raw[raw['Review Sequence'].isin(['L', 'EL', 'REL'])][list(col_des.keys())].rename(columns=col_des)  # keep lastest
            raw['country'] = raw['country'].apply(lambda x: x.title())

            df = prog_dummy(raw)
            super().__init__(df, *args, **kwargs)

        self.dbtype = dbtype

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
        return  df

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
    d = a.expand(start='T-2')
    e = a.roc2025
