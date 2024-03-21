import pandas as pd
import os
from pandaspro import FramePro
from datetime import datetime
from sprnldata.core.mona.config import *

def _getlatestv(tab='d'):
    files = os.listdir(dbpath)
    dates = []
    for file in files:
        if file.endswith('.xlsx') and not file.startswith('~$'):
            tabname, date = file.split('_')
            if tabname == monatab[tab]:
                date = datetime.strptime(date.replace('.xlsx',''), '%Y-%m-%d')
                dates.append(date)
    return f"{monatab[tab]}_{datetime.strftime(max(dates), '%Y-%m-%d')}.xlsx"


class MonaData(FramePro):
    def __init__(self, version='latest', tab='d', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if version == 'latest':
            filename = _getlatestv(tab=tab)
        else:
            filename = f'{monatab[tab]}_{version}.xlsx'
        df = pd.read_excel(f'{dbpath}\{filename}')


if __name__ == '__main__':
    a = MonaData()