from swxl.pandaspro.core import pwread

countrydummy_file = r'Q:\DATA\SPRNL\Users\NL RA\Country Code & Template\Country Code & Grouping\xlarchive\xldummies.xlsx'
programdummy_file = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\General - SPR-SPRNL-2024 ROC – Diagnostic chapter\Data\ROC base sample.xlsx'

dummyc = pwread(countrydummy_file)[0]
w_aggregate = dummyc.inlist('w_aggregate',1)['ifscode'].tolist()
wo_aggregate = dummyc.inlist('wo_aggregate',1)['ifscode'].tolist()

# dummyp = pwread(programdummy_file, )