dbpath = r'Q:\DATA\SPRNL\Users\NL RA\Databases\MONA'

monatab = {
    'd': 'Description',
    'p': 'Purchases',
    'qpc': 'QPC',
    'it': 'QPCandIndTarg',
    'sb': 'Combined'
}

col_des = {
 'Arrangement Number': 'arrnum',
 'Country Name': 'country',
 'Country Code': 'ifscode',
 'Arrangement Type': 'facility',
 'Account': 'account',
 'Approval Date': 'app_date',
 'Approval Year': 'app_year',
 'T': 'T',
 'Initial End date': 'init_end_date',
 'Initial End Year': 'init_end_year',
 'Actual End Date': 'end_date',
 'Actual End Year': 'end_year',
 'Totalaccess': 'amount',
 'Precautionary': 'precaution',
 'Cancelled': 'cancel'}

account_map = {
    'GRA': ['SBA', 'EFF', 'RFI', 'SLL', 'PLL', 'FCL', 'PCI', 'PCL'],
    'PRGT': ['SCF', 'ECF', 'RCF', 'PSI', 'PRGF', 'ESF']
}