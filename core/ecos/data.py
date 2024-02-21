import pandas as pd
import sprnldata.core.ecos.config as c
from swxl.pandaspro.core import pwread

# Step 1: read excel of Data Pulling Tool Main Dashboard
# Step 2: retrieve the meta info into a dictionary
# Step 3: parse dictionary and use it with imf_datatools to download data

class ecosdata(pd.DataFrame):
    def __init__(self, file=None, *args, **kwargs):

        data1 = pwread()
        data2
        data = imf
        # get data from imfdata tools => data
        # data = {..}
        super().__init__(data, *args, **kwargs)
    pass




