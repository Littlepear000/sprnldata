import pandas as pd
from sprnldata.myclass.base import ImfFrame
from sprnldata.downloads.weovintage import folder_vintage
from sprnldata.utils.core import get_latest_file, keep_var


class WeoVinage(ImfFrame):
    def __init__(self,
                 *args,
                 version='latest',
                 **kwargs
                 ):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            local_version = get_latest_file(folder_vintage) if version == 'latest' else version
            raw = pd.read_csv(f'{folder_vintage}/WEOvintages_{local_version}.csv')
            super().__init__(raw)

        self.idvar = ['ifscode', 'vintage_year', 'year']

    @property
    def _constructor(self):
        return WeoVinage

    def keep(self, varlist: str | list, regularvars: list = None):
        if regularvars is None:
            regularvars = self.idvar
        df = keep_var(self, varlist=varlist, regularvars=regularvars)
        return df


if __name__ == '__main__':
    a = WeoVinage(version='latest')
    b = a.df
    c = a.keep(['ngdpd', 'pfb_gdp', 'iar_bmgs'])