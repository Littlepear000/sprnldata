from sprnldata.myclass.mona.ClassDescription import MonaDes
from sprnldata.report.DfAnalysis import DfAnalysis
import sprnldata.report.ROC2025.config_roc2025 as conf


def roc2025_mona_engine(df):
    df.loc[df['arrnum'].isin(conf.roc2018), 'roc2018'] = 1
    df.loc[df['arrnum'].isin(conf.roc2025), 'roc2025'] = 1
    df.loc[df['arrnum'].isin(conf.dr), 'dr'] = 1
    return df

class rocMona(DfAnalysis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dmona_raw = MonaDes(version=self.monav)
        self.dmona = roc2025_mona_engine(self.dmona_raw)

    @property
    def _constructor(self):
        return rocMona

    @property
    def roc2018_list(self):
        return self.dmona[self.dmona['roc2018'] == 1]['arrnum'].to_list()

    @property
    def roc2025_list(self):
        return self.dmona[self.dmona['roc2025'] == 1]['arrnum'].to_list()


roc2018_list = rocMona().roc2018_list
roc2025_list = rocMona().roc2025_list


if __name__ == '__main__':
    a = rocMona().dmona
    # b = a.expand(start='T-5', end='T+5')
    # c = b.df
