from sprnldata.core.frame import ImfFrame
import pandas as pd

countrydummy_file = r'Q:\DATA\SPRNL\Users\NL RA\Country Code & Template\Country Code & Grouping\xlarchive\xldummies.xlsx'
programdummy_file = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\General - SPR-SPRNL-2024 ROC – Diagnostic chapter\Data\ROC base sample.xlsx'

w_aggregate = ImfFrame(pd.read_excel(countrydummy_file)).inlist('w_aggregate', 1)['ifscode'].tolist()
wo_aggregate = ImfFrame(pd.read_excel(countrydummy_file)).inlist('wo_aggregate', 1)['ifscode'].tolist()