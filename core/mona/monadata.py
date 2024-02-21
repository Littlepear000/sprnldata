from swxl.pandaspro.core import pwread
from core.mona.mona_config import *


def monaload(version='latest', tab='D', keeplist=default['D']):
    data, mapping = pwread(dbpath + monatabdict[tab] + monameta[version] + '.xlsx')
    data = data[keeplist]
    data.rename(columns=monarename, inplace=True)
    data['programid'] = data['ifscode'].astype('int').astype('str') + data['appdate'].dt.strftime('%Y%m%d')
    data['month'] = data['appdate'].dt.month
    data['day'] = data['appdate'].dt.day
    data['amount_int'] = round(data['amount'], 0)
    data.loc[data['precautionary'].str.strip() == 'Y', 'precautionary_dummy'] = 1
    data.loc[data['precautionary_dummy'] != 1, 'precautionary_dummy'] = 0
    data.loc[data['cancel'].str.strip() == 'Y', 'cancel_dummy'] = 1
    data.loc[data['cancel_dummy'] != 1, 'cancel_dummy'] = 0
    data.loc[data['year'] <= 2019, 'period'] = 'Pre-Pandemic'
    data.loc[data['year'] > 2019, 'period'] = 'Post-Pandemic'
    data.loc[data.inlist('facility', "PCI", "EFF", "SBA", "PLL", "PCL", "FCL", "SLL", otype='m'), 'account'] = 'GRA'
    data.loc[data.inlist('facility', "PSI", "ECF", "PRGF", "SCF", "ESF", otype='m'), 'account'] = 'PRGT'
    data.loc[data['facility'].str.contains('-'), 'account'] = 'PRGT'
    return data

def monapload(version='latest', tab='P', keeplist=default['P']):
    data, mapping = pwread(dbpath + monatabdict[tab] + monameta[version] + '.xlsx')
    data = data[keeplist]
    return data