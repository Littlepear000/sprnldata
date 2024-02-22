from swxl.pandaspro.core import pwread
from openpyxl.utils import column_index_from_string, get_column_letter
import pandas as pd
import imf_datatools
import numpy as np
import xlwings as xw

template = r'C:\ProgramData\anaconda3\Lib\sprnldata\core\ecos\dev-template.xlsx'
dummyfile = r'Q:\DATA\SPRNL\Users\NL RA\Country Code & Template\Country Code & Grouping\xlarchive\xldummies.xlsx'
dummy = pwread(dummyfile)[0]
wb = xw.Book(template)
ws = wb.sheets['Dashboard']

sectioncol = ['B', 'F', 'J', 'N', 'R']
df = pd.DataFrame()
df['COUNTRY'] = ''
df['dates']=''

for col in sectioncol:
    dbname = ws.range(f'{col}3').value
    colindex = column_index_from_string(col)
    if dbname is not None:
        freq = ws.range(f'{col}4').value
        start = ws.range(f'{col}5').value
        end = ws.range(f'{col}6').value
        countryselect = ws.range(f'{col}7').value

        if countryselect == 'All countries w/o aggregates':
            clist = [512,914,612,614,311,213,911,314,193,122,912,313,419,513,316,913,124,339,638,514,218,963,616,223,516,918,748,618,522,622,156,624,626,628,228,924,233,632,636,634,238,662,960,423,935,128,611,321,243,248,469,253,642,643,939,644,819,172,132,646,648,915,134,652,174,328,258,656,654,336,263,268,532,944,176,534,536,429,433,178,436,136,343,158,439,916,664,826,542,967,443,917,544,941,446,666,668,672,946,137,546,962,674,676,548,556,678,181,867,682,684,273,868,921,948,943,686,688,518,728,836,558,138,196,278,692,694,142,449,564,565,283,853,288,293,566,964,182,359,453,968,922,714,862,135,716,456,722,942,718,724,576,936,961,813,726,199,733,184,524,361,362,364,732,366,734,144,146,463,528,923,738,578,537,742,866,369,744,186,925,869,746,926,466,112,111,298,927,846,299,582,474,754,698,487]
        elif countryselect == 'All countries w aggregates (WLD, WAEMU, EURO, and ECCU)':
            clist = [1,512,914,612,614,311,213,911,314,193,122,912,313,419,513,316,913,124,339,638,514,218,963,616,223,516,918,748,618,522,622,156,624,626,628,228,924,233,632,636,634,238,662,960,423,935,128,611,321,243,248,469,253,642,643,939,644,819,172,132,646,648,915,134,652,174,328,258,656,654,336,263,268,532,944,176,534,536,429,433,178,436,136,343,158,439,916,664,826,542,967,443,917,544,941,446,666,668,672,946,137,546,962,674,676,548,556,678,181,867,682,684,273,868,921,948,943,686,688,518,728,836,558,138,196,278,692,694,142,449,564,565,283,853,288,293,566,964,182,359,453,968,922,714,862,135,716,456,722,942,718,724,576,936,961,813,726,199,733,184,524,361,362,364,732,366,734,144,146,463,528,923,738,578,537,742,866,369,744,186,925,869,746,926,466,112,111,298,927,846,299,582,474,754,698,487,759,163,309]
        else:
            clist_colindex = colindex - 1
            clist_col = get_column_letter(clist_colindex)
            clist = pwread(template, 'Dashboard', f'{clist_col}9:{clist_col}209', firstrow=False)[0][clist_col.lower()].to_list()

        counterlist = pwread(template, 'Dashboard', f'{col}9:{col}209', firstrow=False)[0][col.lower()].to_list()
        indllist_colindex =  colindex + 1
        indllist_col = get_column_letter(indllist_colindex)
        indlist = pwread(template, 'Dashboard', f'{indllist_col}9:{indllist_col}209', firstrow=False)[0][indllist_col.lower()].dropna().to_list()

        data = imf_datatools.get_ecos_sdmx_data(dbname, clist, indlist, freq=freq, longformat=True)
        if start is not None:
            data = data[data['dates'].dt.year >= start]
        if end is not None:
            data = data[data['dates'].dt.year <= end]
        df = pd.merge(df, data, on=['COUNTRY', 'dates'], how='outer')
    else:
        continue

df.rename(columns={'COUNTRY':'ifscode'}, inplace=True)
df['ifscode'] = df['ifscode'].astype(int)
final = pd.merge(df, dummy, on='ifscode', how='left')