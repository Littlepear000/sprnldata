import pandas as pd
import numpy as np
from pandaspro import FramePro


countrydummy_file = r'Q:\DATA\SPRNL\Users\NL RA\Country Code & Template\Country Code & Grouping\xlarchive\xldummies.xlsx'

# Country lists
w_aggregate = FramePro(pd.read_excel(countrydummy_file)).inlist('w_aggregate', 1)['ifscode'].tolist()
wo_aggregate = FramePro(pd.read_excel(countrydummy_file)).inlist('wo_aggregate', 1)['ifscode'].tolist()


class Dummy(FramePro):

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            data = pd.read_excel(countrydummy_file)
            data['emde'] = data['income_emde'].replace(1, 'EMDE').replace(0, np.nan)
            super().__init__(data)

if __name__ == '__main__':
    a = Dummy()
    b = a.df[['ifscode', 'emde']]

