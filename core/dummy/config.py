from sprnldata.core.frame import ImfFrame
import pandas as pd
from datetime import datetime

countrydummy_file = r'Q:\DATA\SPRNL\Users\NL RA\Country Code & Template\Country Code & Grouping\xlarchive\xldummies.xlsx'

# Country lists
w_aggregate = ImfFrame(pd.read_excel(countrydummy_file)).inlist('w_aggregate', 1)['ifscode'].tolist()
wo_aggregate = ImfFrame(pd.read_excel(countrydummy_file)).inlist('wo_aggregate', 1)['ifscode'].tolist()


