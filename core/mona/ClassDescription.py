import pandas as pd
import pandaspro as cpd
from sprnldata.core.mona.config import *
from sprnldata.core.mona.data import MonaData, getlatestv
from sprnldata.core.dummy.config import roc2018raw, roc2025raw

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


class MonaDes(MonaData):
    def __init__(self, *args, version='latest', **kwargs):
        super().__init__(*args, **kwargs)
        self.dbtype = 'd'
        if self.empty:
            if version == 'latest':
                filename = getlatestv(tab=self.dbtype)
            else:
                filename = f'{monatab[self.dbtype]}_{version}.xlsx'

            raw = pd.read_excel(f'{dbpath}/{filename}')
            raw['Review Sequence'] = raw['Review Sequence'].apply(lambda x: x.strip())
            raw['Account'] = raw['Arrangement Type'].apply(lambda x: account_match(x) if x.find('-') < 0 else 'PRGT')
            raw['Actual End Date'] = raw.apply(
                lambda row: row['Initial End date'] if pd.isna(row['Revised End Date']) else row['Revised End Date'],
                axis=1)
            raw['Actual End Year'] = raw['Actual End Date'].dt.year
            raw['T'] = raw.apply(
                lambda row: row['Approval Year'] + 1 if row['Approval Date'].quarter == 4 else row['Approval Year'],
                axis=1)
            raw = raw[raw['Review Sequence'].isin(['E', 'EL', 'REL'])][list(col_des.keys())].rename(
                columns=col_des)  # keep lastest
            raw['country'] = raw['country'].apply(lambda x: x.title())

            df = prog_dummy(raw)

            for col, values in df.items():
                self[col] = values

    @property
    def _constructor(self):
        return MonaDes


if __name__ == '__main__':
    a = MonaDes(version='2024-01-24')
