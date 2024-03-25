import os
from pandaspro import FramePro
from datetime import datetime
from sprnldata.core.mona.config import *
from sprnldata.core.frame import ImfFrame


def getlatestv(tab='d'):
    files = os.listdir(dbpath)
    dates = []
    for file in files:
        if file.endswith('.xlsx') and not file.startswith('~$'):
            tabname, date = file.split('_')
            if tabname == monatab[tab]:
                date = datetime.strptime(date.replace('.xlsx',''), '%Y-%m-%d')
                dates.append(date)
    return f"{monatab[tab]}_{datetime.strftime(max(dates), '%Y-%m-%d')}.xlsx"


class MonaData(ImfFrame):
    pass


if __name__ == '__main__':
    # a = getlatestv(tab='d')
    b = MonaData({'a': [1, 2, 3], 'b': [3, 4, 5]})