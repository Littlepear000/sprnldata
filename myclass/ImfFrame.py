import pandas as pd
import re
from pandaspro.core.frame import FramePro
from sprnldata.myclass.dummy import Dummy


def filter_year(df, years: str, ftype: str):
    ftype_dict = {
        'y': 'year',
        'v': 'vintage_year',
        's': 'app_year',
        'e': 'end_year'
    }
    if re.fullmatch(r'\d{4}', years):
        keepkey = int(re.fullmatch(r'(\d{4})', years).group(1))
        print(ftype_dict[ftype], keepkey)
        return df.inlist(ftype_dict[ftype], keepkey)
    elif re.fullmatch(r'\d{4}_\d{4}', years):
        startyear = int(re.fullmatch(r'(\d{4})_(\d{4})', years).group(1))
        endyear = int(re.fullmatch(r'(\d{4})_(\d{4})', years).group(2))
        return df.inlist(ftype_dict[ftype], [i for i in range(startyear, endyear + 1)])
    elif re.fullmatch(r'(\d+)', years):
        numbers = re.fullmatch(r'(\d+)', years).group(1)
        if len(numbers) % 4 == 0:
            return df.inlist(ftype_dict[ftype], years)
        else:
            raise ValueError(
                'Enter separate years in 4-digit format, eg. 200120042008 for year 2001, 2004 and 2008')
    else:
        raise ValueError('Invalid years input in para')


class ImfFrame(FramePro):
    def __getattr__(self, item):
        if (re.fullmatch(r'[yvse]\d{4}', item) or
                re.fullmatch(r'[yvse]\d{4}_\d{4}', item) or
                re.fullmatch(r'[yvse]\d+', item)):
            ftype = item[0]
            years = item[1:]
            return filter_year(self, years=years, ftype=ftype)
        # Inlist with Dummies
        elif item in ['keep2018', 'keep2025']:
            return self.inlist(item.replace('keep', 'roc'), 1)
        elif item in self.columns and item not in self.idvar:
            return self[self.idvar + [item]]
        elif item in ['idvar', 'dmona', 'dmona_raw']:
            pass
        else:
            return super().__getattr__(item)

    @property
    def dummy(self):
        countrydummy = Dummy()
        return pd.merge(self, countrydummy, on='ifscode', how='left')

    def create_boxplot_data(self):
        self.expand

if __name__ == '__main__':
    a = FramePro().expand_column