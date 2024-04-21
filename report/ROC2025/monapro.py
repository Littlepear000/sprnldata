from sprnldata import MonaDes
from sprnldata.report.analyse import analyse
import sprnldata.report.ROC2025.config_roc2025 as conf


def roc2025_mona_engine(df):
    df.loc[df['arrnum'].isin(conf.roc2018), 'roc2018'] = 1
    df.loc[df['arrnum'].isin(conf.roc2025), 'roc2025'] = 1
    df.loc[df['arrnum'].isin(conf.dr), 'dr'] = 1
    return df

class monapro(analyse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dmona_raw = MonaDes(version=self.monav)
        self.dmona = roc2025_mona_engine(self.dmona_raw)


if __name__ == '__main__':
    a = monapro().dmona
    b = a.expand(start='T-5', end='T+5')
    c = b.df
