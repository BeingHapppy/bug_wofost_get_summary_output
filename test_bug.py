# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 21:46:21 2021

@author: WYTNBQ
"""
import os
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", 250)

from pcse.models import Wofost71_PP
from pcse.base import ParameterProvider
from pcse.fileinput import YAMLCropDataProvider
from pcse.util import WOFOST71SiteDataProvider
from pcse.fileinput import CABOFileReader
from pcse.fileinput import YAMLAgroManagementReader
from pcse.fileinput import CABOWeatherDataProvider

# In[]

data_dir = './'

cropfile = os.path.join(data_dir, 'cropdata') 
cropd = YAMLCropDataProvider(cropfile)
cropd.set_active_crop('wheat', "Winter_wheat_105")  # I changed the wheat file from de vit Allard for local setting


# In[]
soild = CABOFileReader('Hebi_WYT.soil')

# In[]

sited = WOFOST71SiteDataProvider(
        IFUNRN = 0,
        SSMAX  = 0.000000, 
        WAV    = 20.000000, 
        NOTINF = 0.000000,
        SSI    = 0.000000, 
        SMLIM  = 0.500000,
        CO2    = 360.)
# In[]

wdp = CABOWeatherDataProvider('114.3_35.7')
   
agro=YAMLAgroManagementReader('Hebi_2019_V2-3_L1.amgt')

# In[]

params = ParameterProvider(cropdata=cropd, sitedata=sited, soildata=soild)
      
wofost = Wofost71_PP(params, wdp, agro)
wofost.run_till_terminate()

summerout = wofost.get_summary_output()
print(summerout)  # which should have content, but now it is []

df = pd.DataFrame(wofost.get_output()).set_index("day") 