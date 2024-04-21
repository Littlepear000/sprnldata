import pandas as pd
import imf_datatools
import datetime
import time
import sprnldata.core.dummy.config as dum


vintagelist = [
    'WEO_WEOApr2002Pub',
    'WEO_WEOApr2003Pub',
    'WEO_WEOApr2004Pub',
    'WEO_WEOApr2005Pub',
    'WEO_WEOApr2006Pub',
    'WEO_WEOApr2007Pub',
    'WEO_WEOApr2008Pub',
    'WEO_WEOApr2009Pub',
    'WEO_WEOApr2010Pub',
    'WEO_WEOApr2011Pub',
    'WEO_WEOApr2012Pub',
    'WEO_WEOApr2013Pub',
    'WEO_WEOApr2014Pub',
    'WEO_WEOApr2015Pub',
    'WEO_WEOApr2016Pub',
    'WEO_WEOApr2017Pub',
    'WEO_WEOApr2018Pub',
    'WEO_WEOApr2019Pub',
    'WEO_WEOApr2020Pub',
    'WEO_WEOApr2021Pub',
    'WEO_WEOApr2022Pub',
    'WEO_WEOApr2023Pub',
    'WEO_WEOApr2024Pub',
]

varlist = [
    'NGDP',
    'NGDPD',
    'GGR',
    'GGRT',
    'GGRG',
    'GGRSS',
    'GGX',
    'GGEI',
    'GGXWDG',
    'GGR_GDP',
    'GGX_GDP',
    'GGEI_GDP',
    'BCA_GDP_BP6',
    'BFD_GDP_BP6',
    'BMGS_BP6',
    'IAR_BP6',
    'GGXCNL_GDP',
    'GGXWDG_GDP',
    'NGDP_RPCH',
    'PCPI_PCH',
]

# This process takes about 10-15min
def pull_vintage(var_list):
    starttime = time.time()

    df = pd.DataFrame()
    for database in vintagelist:
        print(database)
        dfweo = imf_datatools.get_ecos_sdmx_data(database, dum.wo_aggregate, var_list, freq='A', longformat=True)
        if not isinstance(dfweo, pd.DataFrame):
            continue
        dfweo['vintage_year'] = int(database[10:14])
        df = pd.concat([df, dfweo], ignore_index=True)
        
    df['year'] = df['dates'].dt.year
    df.rename(columns={'COUNTRY': 'ifscode'}, inplace=True)
    df.columns = df.columns.str.lower().str.replace('.a', '', regex=False)
    df = df[['ifscode', 'vintage_year', 'year'] + [var.lower() for var in var_list]]

    ### Generate commonly used variables
    df['pfb_gdp'] = (df['ggr'] - df['ggx'] + df['ggei']) / df['ngdp'] * 100     # Primary fiscal balance
    df['iar_bmgs'] = df['iar_bp6'] / (df['bmgs_bp6'] / 12)     # Reserves in months of imports

    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    df.to_csv(f'C:/Users/xli7/OneDrive - International Monetary Fund (PRD)/Databases/ECOS/WEOvintages/WEOvintages_{timestamp}.csv', index=False)
    endtime = time.time()
    print(f'Download complete. Time Duration: {round((endtime-starttime)/60, 1)}min')


if __name__ == '__main__':
    # vintagelist = ['WEO_WEOApr2024Pub', 'WEO_WEOApr2024Pub']
    # varlist = ['GGR', 'GGX', 'GGEI', 'IAR_BP6', 'BMGS_BP6', 'NGDP']
    pull_vintage(varlist)
