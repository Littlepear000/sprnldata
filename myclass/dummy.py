import pandas as pd
import numpy as np
from pandaspro import FramePro
from pandaspro.cpdbase.cpd_base_frame import cpdBaseFrame


dummy_path = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Databases\Dummy'


@cpdBaseFrame(path=dummy_path, file_type='xlsx')
class Dummy(FramePro):

    @property
    def emde(self):
        return self.inlist('income_emde', 1)['ifscode'].tolist()

    @property
    def w_aggregate(self):
        return self.inlist('w_aggregate', 1)['ifscode'].tolist()

    @property
    def wo_aggregate(self):
        return self.inlist('wo_aggregate', 1)['ifscode'].tolist()


if __name__ == '__main__':
    from sprnldata.myclass.country_grouping import CountryGrouping as cg
    a = Dummy()
    b = cg().get_by_groupcode(200)
    c = a.inlist('ifscode', b, engine='c', rename='emde').df
    # b = a.df[['ifscode', 'emde']]

