from swxl.pandaspro.core import pwread
from sprnldata.core.frame import ImfFrame
import sprnldata.core.dummy.config as c
import pandas as pd
from pandaspro import FramePro

class Dummy(ImfFrame):

    @staticmethod
    def _getdummy(engine='country'):
        if engine == 'country':
            dummyraw = pwread(c.countrydummy_file)[0]
            # w_aggregate = dummyc.inlist('w_aggregate', 1)['ifscode'].tolist()
            # wo_aggregate = dummyc.inlist('wo_aggregate', 1)['ifscode'].tolist()
        else:
            dummyraw = pwread(c.programdummy_file, 'ROC2024')[0]
        return dummyraw

    def __init__(self, data=None, engine='country', *args, **kwargs):
        if isinstance(data, (pd.DataFrame, FramePro)):
            super().__init__(data=data, *args, **kwargs)
        else:
            result = Dummy._getdummy(engine=engine)
            super().__init__(data=result, *args, **kwargs)

if __name__ == '__main__':
    a = Dummy()
    b = a.inlist('ifscode', 111)

