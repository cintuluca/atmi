## @file src/sampling.py
# @brief Generator of the statistical resampling for the atmospheric variables.
#
# Python script necessary to extract the probability density function from the climatic data and to perform a correlated resampling for the given time period.
#
# The file is located under atmi/src.

from lib import atmsampling
from lib import netCDFutils
from datetime import datetime
import numpy as np
import os
import pandas as pd
import sys
from tqdm import tqdm
import xarray as xr

with open(os.path.expanduser('~')+'/.atmi') as file:
    DIR = file.readline().strip('\n')   # Global path of the project

## Reading the configuration file
#################################
conf_file = sys.argv[1]
if os.path.exists(conf_file) == False:
	print('Directory not found!')
	sys.exit()
	
with open(conf_file) as f:
	args = f.readlines()
	args = [arg.rstrip('\n') for arg in args]
datafiles, var, month1, day1, hour1, month2, day2, hour2, lat, lon, N, filename = args
datafiles = datafiles.split(',')
var = var.split(',')

for i in range(len(datafiles)):
    print('Datafile\t->\t'+datafiles[i])
    if os.path.exists(datafiles[i]) == False:
	    print('Directory not found!')
	    sys.exit()
	
    data = netCDFutils.data(datafiles[i])   # opening dataset
    names = data.variables()

    print('Varible\t\t->\t'+var[i])
    if names.count(var[i]) == 0:
        print('Variable name not valid!')
        sys.exit()

days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
print('Starting Month\t->\t'+month1)
if (float(month1) != int(month1)) or (float(month1) <= 0) or (float(month1) > 12):
	print('Month not valid!')
	sys.exit()

print('Starting Day\t->\t'+day1)
if (float(day1) != int(day1)) or (float(day1) < 0) or (float(day1) > days[int(month1)-1]):
        print('Day not valid!\n')
        sys.exit()

print('Starting Hour\t->\t'+hour1)
if (float(hour1) != int(hour1)) or (float(hour1) < 0) or (float(hour1) > 23):
        print('Hour not valid!\n')
        sys.exit()
        
print('Final Month\t->\t'+month2)
if (float(month2) != int(month2)) or (float(month2) <= 0) or (float(month2) > 12):
	print('Month not valid!')
	sys.exit()

print('Final Day\t->\t'+day2)
if (float(day2) != int(day2)) or (float(day2) < 0) or (float(day2) > days[int(month2)-1]):
        print('Day not valid!\n')
        sys.exit()

print('Final Hour\t->\t'+hour2)
if (float(hour2) != int(hour2)) or (float(hour2) < 0) or (float(hour2) > 23):
        print('Hour not valid!\n')
        sys.exit()

print('Latitude\t->\t'+lat)
print('Longitude\t->\t'+lon)
lat, lon = [float(lat), float(lon)]

print('N° Samplings\t->\t'+N)
if (float(N) < 0) or (float(N) != int(N)):
    print('N not valid!\n')
    sys.exit()
N = int(N)
    
print('Filename\t->\t'+filename+'\n')
#################################
    
## Initializing the realizations sampling
#########################################
date1 = np.datetime64(str(1981)+'-'+str(month1)+'-'+str(day1)+'T'+str(hour1))   # arbitrary non-leap year
date2 = np.datetime64(str(1981)+'-'+str(month2)+'-'+str(day2)+'T'+str(hour2))	# arbitrary non-leap year
hours = (date2 - date1) // np.timedelta64(1,'h')

datas = []
for datafile in datafiles:
    datas.append(netCDFutils.data(datafile))
    
start, stop = np.min([data.start for data in datas]), np.min([data.stop for data in datas])

atmospheres, ms, ds, hs = [], [], [], []
for h in tqdm(range(hours + 1), desc='Loading ...'):
    date = date1 + np.timedelta64(h, 'h')
    mdh = [pd.to_datetime(date).month, pd.to_datetime(date).day, pd.to_datetime(date).hour]
    for i in range(len(mdh)):
        if mdh[i] <= 1 or np.log10(mdh[i]) < 1: # controlling the formatting for window function
            mdh[i] = '0'+str(mdh[i])
        mdh[i] = str(mdh[i])
    month, day, hour = mdh
    ms.append(month), ds.append(day), hs.append(hour)

    window = netCDFutils.window(start + 1, stop - 1, month, day, hour, 4)
    
    variables = []
    for i in range(len(var)):
        values = datas[i].values(lat, lon, window, var[i])
        variables.append(atmsampling.variable(var[i], values))
        
    atmospheres.append(atmsampling.atmosphere(variables))
atm = atmsampling.samplings(atmospheres)
#########################################

## Writing the results on a .csv file
#####################################
samplings = atm.correlated_sample(N)

n = 0   # counter for the samplings name
for sampling in samplings:
    df = pd.DataFrame(sampling, columns=var)
    df.insert(0, 'Month', ms), df.insert(1, 'Day', ds), df.insert(2, 'Hour', hs)

    if os.path.exists(DIR+'/outputs/sampling/'+filename+str(n)+'.csv') == True:
	    with open(DIR+'/outputs/sampling/'+filename+str(n)+'.csv', 'r+') as f:
		    f.truncate(0)

    with open(DIR+'/outputs/sampling/'+filename+str(n)+'.csv', 'a') as f:
	    f.write('# '+str(datetime.now())+'\n\n')
	    df.to_csv(f)
	
    print('Sampling file saved in '+DIR+'/outputs/sampling'+filename+str(n)+'.csv!')
    n = n + 1
#####################################
