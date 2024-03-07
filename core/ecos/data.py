from sprnldata.core.frame import ImfFrame
from pandaspro.core.frame import FramePro
from swxl.pandaspro.core import pwread
from openpyxl.utils import column_index_from_string, get_column_letter
import pandas as pd
import imf_datatools
import xlwings as xw
import sprnldata.core.dummy.config as dum
import sprnldata.core.ecos.config as c
import os
import shutil


# Step 1: read excel of Data Pulling Tool Main Dashboard
# Step 2: retrieve the meta info into a dictionary
# Step 3: parse dictionary and use it with imf_datatools to download data

def _ecosuse(file=c.template):
    wb = xw.Book(file)
    ws = wb.sheets['Dashboard']

    sectioncol = ['B', 'F', 'J', 'N', 'R']
    df = pd.DataFrame()
    df['COUNTRY'] = ''
    df['dates'] = ''
    errmsg = ''

    for col in sectioncol:
        dbname = ws.range(f'{col}3').value
        colindex = column_index_from_string(col)
        if dbname is not None:
            freq = ws.range(f'{col}4').value
            start = ws.range(f'{col}5').value
            end = ws.range(f'{col}6').value
            countryselect = ws.range(f'{col}7').value

            if countryselect == 'All countries w/o aggregates':
                clist = dum.wo_aggregate
            elif countryselect == 'All countries w aggregates (WLD, WAEMU, EURO, and ECCU)':
                clist = dum.w_aggregate
            else:
                clist_colindex = colindex - 1
                clist_col = get_column_letter(clist_colindex)
                clist = pwread(c.template, 'Dashboard', f'{clist_col}10:{clist_col}209', firstrow=False)[0][
                    clist_col.lower()].to_list()

            counterlist = pwread(c.template, 'Dashboard', f'{col}10:{col}209', firstrow=False)[0][
                col.lower()].to_list()
            indlist_colindex = colindex + 1
            indlist_col = get_column_letter(indlist_colindex)
            indlist = pwread(c.template, 'Dashboard', f'{indlist_col}10:{indlist_col}209', firstrow=False)[0][
                indlist_col.lower()].dropna().to_list()

            data = imf_datatools.get_ecos_sdmx_data(dbname, clist, indlist, freq=freq, longformat=True)
            ## print notification message including time duration for pulling the data
            if data is not None:
                if start is not None:
                    data = data[data['dates'].dt.year >= start]
                if end is not None:
                    data = data[data['dates'].dt.year <= end]
                df = pd.merge(df, data, on=['COUNTRY', 'dates'], how='outer')
            else:
                errmsg = errmsg + '\n' + dbname + ': ' + ', '.join(indlist) + '\n'
        else:
            continue

    print(errmsg)
    df.rename(columns={'COUNTRY': 'ifscode'}, inplace=True)
    df['ifscode'] = df['ifscode'].astype(int)
    df['year'] = df['dates'].dt.year
    df.drop(columns='dates', inplace=True)
    # reorder the columns
    first_columns = ['ifscode', 'year']
    remaining_columns = [col for col in df.columns if col not in first_columns]
    new_order = first_columns + remaining_columns
    return df[new_order]

class EcosData(ImfFrame):
    def __init__(self, data=None, *args, **kwargs):
        if isinstance(data, (pd.DataFrame, FramePro)):
            super().__init__(data=data, *args, **kwargs)
        else:
            file = data if data is not None else c.template
            result = _ecosuse(file=file)
            super().__init__(data=result, *args, **kwargs)


class EcosSet:
    def __init__(self, workbook: str = 'Data Pulling Template.xlsx'):
        destination_file = os.path.join(os.getcwd(), workbook)
        if os.path.exists(destination_file):
            xw.Book(destination_file)
            raise FileExistsError(f'Error: {workbook} already exists! Opening, please go ahead and check ... ')
        else:
            shutil.copyfile(c.template, destination_file)

        self.path = os.path.join(os.getcwd(), workbook)
        xw.Book(self.path)

    def pull(self):
        return EcosData(self.path)


if __name__ == '__main__':
    a = EcosSet('template1.xlsx')
    df = a.pull()
    df.to_excel('temp.xlsx', index=False)
    df.lowervarlist()

    import re

    test = pd.DataFrame({'A': [1, 2, 3], 'a': [2, 3, 4], 'B': [3, 4, 5]})
    oldname = test.columns.to_list()
    pattern = re.compile('\W+')

    # Dictionary to track the occurrence of each formatted column name
    name_count = {}
    newname = []
    for name in oldname:
        # Format the column name
        formatted_name = re.sub(pattern, '_', str(name)).lower().strip("_")

        # Increment count and modify name if it's a duplicate
        if formatted_name in name_count:
            name_count[formatted_name] += 1
            formatted_name += f"_{name_count[formatted_name]}"
        else:
            name_count[formatted_name] = 0

        newname.append(formatted_name)
