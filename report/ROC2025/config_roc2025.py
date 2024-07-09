import pandas as pd
from sprnldata.config import onedrive_root

# root path does not need to change
root_path = fr'{onedrive_root}'

project_path = root_path + '/General - SPR-SPRNL-2024 ROC – Diagnostic chapter'

rocdummy_file = project_path + '/Data/ROC base sample.xlsx'
programdummy_file = project_path + '/Data/Macroeconomic output/raw data/Dummies_program with debt restructure.xlsx'

# ROC Dummies
roc2025 = pd.read_excel(rocdummy_file, 'ROC2024').sort_values('Arrangement Number')['Arrangement Number'].to_list()
roc2018 = pd.read_excel(rocdummy_file, 'ROC2018').sort_values('Arrangement Number')['Arrangement Number'].to_list()

# dr = debt restructure
dr = pd.read_excel(programdummy_file, 'DR').sort_values('Arrangement Number')['Arrangement Number'].to_list()

