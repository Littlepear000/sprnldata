from swxl.pandaspro.core import pwread

dummyfile = r'Q:\DATA\SPRNL\Users\NL RA\Country Code & Template\Country Code & Grouping\xlarchive\xldummies.xlsx'
dummy = pwread(dummyfile)[0]
w_aggregate = dummy.inlist('w_aggregate',1)['ifscode'].tolist()
wo_aggregate = dummy.inlist('wo_aggregate',1)['ifscode'].tolist()