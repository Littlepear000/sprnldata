import pandas as pd
import re
from sprnldata.myclass.mona.mona_config import *
from sprnldata.myclass.mona.mona_base import MonaData
from sprnldata.utils.core import get_latest_file


def _engine_monades(version):
    if version == 'latest':
        filename = f'{monatab["d"]}_{get_latest_file(monad_folder)}.xlsx'
    else:
        filename = f'{monatab["d"]}_{version}.xlsx'

    raw = pd.read_excel(f'{monad_folder}/{filename}')
    raw['Review Sequence'] = raw['Review Sequence'].apply(lambda x: x.strip())
    raw['Account'] = raw['Arrangement Type'].apply(lambda x: account_match(x) if x.find('-') < 0 else 'PRGT')
    raw['Actual End Date'] = raw.apply(
        lambda row: row['Initial End date'] if pd.isna(row['Revised End Date']) else row['Revised End Date'], axis=1)
    raw['Actual End Year'] = raw['Actual End Date'].dt.year
    raw['T'] = raw.apply(
        lambda row: row['Approval Year'] + 1 if row['Approval Date'].quarter == 4 else row['Approval Year'], axis=1)
    raw = raw[raw['Review Sequence'].isin(['L', 'EL', 'REL'])][list(col_des.keys())].rename(
        columns=col_des)  # Keep latest
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
                'year_label': 'T' if year == 0 else f'T+{str(year)}' if year > 0 else f'T{str(year)}'})
    else:
        raise ValueError('Parameter "on" only accept "T" or "app_year"')
    return pd.DataFrame(new_rows)


class MonaDes(MonaData):
    def __init__(self, *args, version='latest', **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            df = _engine_monades(
                version=version
            )
            super().__init__(df)
        self.dbtype = 'd'
        self.version = version
        self.idvar = ['arrnum', 'ifscode', 'facility', 'account', 'app_date', 'app_year', 'T', 'end_date', 'end_year']

    @property
    def _constructor(self):
        return MonaDes

    def expand(self, start: str = 'start', end: str = 'end', on: str = 'T'):
        df = pd.concat([expand_rows(row, start=start, end=end, on=on) for _, row in self.iterrows()], ignore_index=True)
        return MonaDes(df)


if __name__ == '__main__':
    a = MonaDes()
    d = a.expand(start='T-5', end='T+5')
    e = a.keep('amount')
