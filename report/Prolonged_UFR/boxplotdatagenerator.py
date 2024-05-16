import pandas as pd
from sprnldata.myclass.api import ecos
from sprnldata.report.Prolonged_UFR.config import combine_group

class BoxplotDataGenerator:
    """
    group: DataFrame or DataFrame's child class
    """
    def __init__(self,
                 group,
                 varname: str | list,
                 year: int):
        wdi = ecos().keep_var(varname)
        wdi = wdi[wdi['year'] == year].drop('year', axis=1)
        pd.merge(group, wdi.df, on='ifscode', how='left')


if __name__ == '__main__':

    a = BoxplotDataGenerator(combine_group, 'si.pov.gini', 2022)
    # df = ecos().wdi
    # b = pd.merge(combine_group, df[df['year'] == 2020].drop('year', axis=1).df, on='ifscode', how='left')
    # b.describe().to_excel('temp.xlsx')