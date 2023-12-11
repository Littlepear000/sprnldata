dbpath = "Q:/DATA/SPRNL/Users/Shelley/databases/mona/raw/"

default = [
    'arrangement_number', 'country_name', 'country_code', 'arrangement_type',
    'approval_date', 'approval_year', 'initial_end_date', 'revised_end_date',
    'review_type', 'review_sequence', 'totalaccess', 'precautionary', 'cancelled'
]

monameta = {
    'latest': '20231210_1930',
    '2023-12-10': '20231210_1930',
    '2023-11-30': '20231130_1500'
}

monatabdict = {
    'D': 'Description',
    'C': 'Combined',
    'M': 'Mecon',
    'P': 'Purchases',
    'Pro': 'Program',
    'Q': 'QPCandIndTarg',
    'QPC': 'QPC',
    'R': 'Reviews'
}

monarename = {
    'arrangement_number': 'arrnum',
    'country_name': 'country',
    'country_code': 'ifscode',
    'arrangement_type': 'facility',
    'approval_date': 'appdate',
    'approval_year': 'year',
    'initial_end_date': 'expdate',
    'revised_end_date': 'expdate_revise',
    'review_type': 'review_type',
    'review_sequence': 'review_seq',
    'totalaccess': 'amount',
    'precautionary': 'precautionary',
    'cancelled': 'cancel'
}

