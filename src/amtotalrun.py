## @file src/amtotalrun.py
# @brief Generator of the am configuration file for the real data.
#
# Python script necessary to calculate the vertical profiles of the atmospheric real data and write the am configuration file.
#
# The file is located under atmi/src.

from lib import amutils
from datetime import datetime
from lib import netCDFutils
import numpy as np
import os
import pandas as pd
from tqdm import tqdm

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
datafiles, var, year1, year2, lat, lon, N ,freq_start, freq_stop, freq_interval, paramsfile, filename = args
datafiles = datafiles.split(',')
var = var.split(',')

starting_years, final_years = [], []
for i in range(len(datafiles)):
    print('Datafile\t\t->\t'+datafiles[i])
    if os.path.exists(datafiles[i]) == False:
	    print('Directory not found!')
	    sys.exit()
	
    data = netCDFutils.data(datafiles[i])   # opening dataset
    names = data.variables()
    starting_years.append(data.start)
    final_years.append(data.stop)

    print('Varible\t\t\t->\t'+var[i])
    if names.count(var[i]) == 0:
        print('Variable name not valid!')
        sys.exit()
       
starting_year = np.max(starting_years)
final_year = np.min(final_years)

print('Starting Year\t\t->\t'+year1)
if (float(year1) != int(year1)) or (float(year1) < 0) or (float(year1) < starting_year):
        print('Starting Year not valid!\n')
        sys.exit()

print('Final Year\t\t->\t'+year2)
if (float(year2) != int(year2)) or (float(year2) < 0) or (float(year2) > final_year):
        print('Final Year not valid!\n')
        sys.exit()

print('Latitude\t\t->\t'+lat)
print('Longitude\t\t->\t'+lon)
lat, lon = [float(lat), float(lon)]

print('N° Layers\t\t->\t'+N)
N = int(N)
print('Starting Frequency\t->\t'+freq_start+'GHz')
print('Ending Frequency\t->\t'+freq_stop+'GHz')
print('Frequency Interval\t->\t'+freq_interval+'GHz')
    
print('Parameters File\t->\t', paramsfile)
print('Filename\t\t->\t'+filename+'\n')
#################################

## Initializing the realizations
################################
datas = []
for datafile in datafiles:
    datas.append(netCDFutils.data(datafile))
    
date1 = np.datetime64(str(year1)+'-01-01T00')
date2 = np.datetime64(str(year2)+'-12-31T23')
hours = (date2 - date1) // np.timedelta64(1,'h')

dates = []
for h in range(hours+1):
    dates.append(date1 + np.timedelta64(h,'h'))
    
data_loc_time = datas[0].dataset.sel(time=dates, longitude=lon, latitude=lat, method='nearest')
variables = {'year': pd.to_datetime(data_loc_time['time'].values).year,
    'month': pd.to_datetime(data_loc_time['time'].values).month,
    'day': pd.to_datetime(data_loc_time['time'].values).day,
    'hour': pd.to_datetime(data_loc_time['time'].values).hour
    }
for i in range(len(datas)):
    data_loc_time = datas[i].dataset.sel(time=dates, longitude=lon, latitude=lat, method='nearest')
    variables[var[i]] = data_loc_time[var[i]].values
    
realizations = pd.DataFrame(variables)
################################

## Saving all the configuration files
#####################################
file = open(DIR+'/am/config/'+filename+'.txt', 'w')
print('\nSaving the configuration files in '+DIR+'/am/config/ ...')
for i in tqdm(range(len(realizations.index)), desc='Loading ...'):
    y, m, d, h = int(realizations.iloc[i]['year']), int(realizations.iloc[i]['month']), int(realizations.iloc[i]['day']), int(realizations.iloc[i]['hour'])
    date = str(y)+'_'+str(m)+'_'+str(d)+'_'+str(h)
    T0, P0, PWV = realizations.iloc[i]['stl1'], realizations.iloc[i]['sp'], realizations.iloc[i]['tcwv']
    Z, T, P, pwv = amutils.profiles(T0, P0, PWV, m, N)
    amutils.config(freq_start, freq_stop, freq_interval, 2.7, Z, T, P, pwv, DIR+'/am/config/'+filename+date)
    file.write(filename+date+'\n')
file.close()
####################################
