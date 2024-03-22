import pandas as pd
from core.mona.config import monatab, dbpath
from sprnldata.core.mona.data import MonaData, getlatestv
import pandaspro

class MonaDes(MonaData):
    def __init__(self, *args, version='latest', **kwargs):
        super().__init__(*args, **kwargs)
        self.dbtype = 'd'
        if self.empty:
            if version == 'latest':
                filename = getlatestv(tab=self.dbtype)
            else:
                filename = f'{monatab[self.dbtype]}_{version}.xlsx'

            df = pd.read_excel(f'{dbpath}/{filename}')

            super().__init__(df, *args, **kwargs)
            self.xlname = 1

    @property
    def _constructor(self):
        return MonaDes


if __name__ == '__main__':
    a = MonaDes(version='2024-01-24')
    # print(a.shape)
    b = MonaDes({'a': [1, 2, 3], 'b': [3, 4, 5]})
    # b = a.inlist('Country Code', 520)
    # print(b.xlname)
