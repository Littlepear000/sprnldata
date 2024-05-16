import pandas as pd

wbiso_replace = {
    'KSV': 'KOS',
    'ADO': 'AND',
    'TMP': 'TLS',
    'ZAR': 'COD',
    'ROM': 'ROU'
}

ufr_root = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\General - SPR-Prolonged UFR\Data\WGI'

# Grouping 1: UFR defined groups
ufr_groupfile = f'{ufr_root}/raw/Repeated User Country Groups.xlsx'
ufr_group = pd.read_excel(ufr_groupfile, sheet_name='group', skiprows=2)
ufr_group['group'] = ufr_group['group'].fillna(method='ffill')

# Grouping 2: EMDE countries
inc_groupfile = f'{ufr_root}/raw/country_grouping_dummies.xlsx'
inc_group = pd.read_excel(inc_groupfile)[['isocode', 'country', 'ifscode', 'income_emde']].rename(columns={'isocode': 'iso', 'income_emde': 'group'})
emde_group = inc_group[inc_group['group'] == 1]
emde_group['group'] = 'EMDE'

combine_group = pd.concat([ufr_group, emde_group])
combine_group['iso'] = combine_group['iso'].replace(wbiso_replace)

