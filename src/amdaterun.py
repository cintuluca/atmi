## @file src/amdaterun.py
# @brief Generator of the am configuration file for the real data (specific dates).
#
# Python script necessary to calculate the vertical profiles of the atmospheric real data and write the am configuration file (specific dates only).
#
# The file is located under atmi/src.

from lib import amutils
from datetime import datetime
from lib import netCDFutils
import numpy as np
import os
import pandas as pd
import sys
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
datafiles, var, dates_file, lat, lon, N ,freq_start, freq_stop, freq_interval, paramsfile, filename = args
datafiles = datafiles.split(',')
var = var.split(',')

starting_dates, final_dates = [], []
for i in range(len(datafiles)):
    print('Datafile\t\t->\t'+datafiles[i])
    if os.path.exists(datafiles[i]) == False:
	    print('Directory not found!')
	    sys.exit()
	
    data = netCDFutils.data(datafiles[i])   # opening dataset
    names = data.variables()
    starting_dates.append(data.dataset['time'].values.min())
    final_dates.append(data.dataset['time'].values.max())

    print('Varible\t\t\t->\t'+var[i])
    if names.count(var[i]) == 0:
        print('Variable name not valid!')
        sys.exit()
      
starting_dates = np.array(starting_dates)
final_dates = np.array(final_dates)

print('Dates File\t\t->\t'+dates_file)
dates_df = pd.read_csv(dates_file, names=['Year','Month','Day','Hour'])
dates = []
for i in range(len(dates_df)):
    ymdh = [dates_df['Year'][i], dates_df['Month'][i], dates_df['Day'][i], dates_df['Hour'][i]]
    for j in range(len(ymdh)):
        if ymdh[j] < 10:
            ymdh[j] = '0'+str(ymdh[j])
        else:
            ymdh[j] = str(ymdh[j])
    dates.append(np.datetime64(ymdh[0]+'-'+ymdh[1]+'-'+ymdh[2]+'T'+ymdh[3]))

dates = np.array(dates)
    
if dates.min() < starting_dates.max() or dates.max() > final_dates.min():
        print('Dates not valid!')
        sys.exit()

print('Latitude\t\t->\t'+lat)
print('Longitude\t\t->\t'+lon)
lat, lon = [float(lat), float(lon)]

print('N° Layers\t\t->\t'+N)
N = int(N)
print('Starting Frequency\t->\t'+freq_start+'GHz')
print('Ending Frequency\t->\t'+freq_stop+'GHz')
print('Frequency Interval\t->\t'+freq_interval+'GHz')
    
print('Parameters File\t\t->\t'+paramsfile)
print('Filename\t\t->\t'+filename+'\n')
#################################

## Initializing the realizations
################################
datas = []
for datafile in datafiles:
    datas.append(netCDFutils.data(datafile))

data_loc_time = datas[0].dataset.sel(time=dates, longitude=lon, latitude=lat, method='nearest')
variables = {'year': pd.to_datetime(data_loc_time['time'].values).year,
    'month': pd.to_datetime(data_loc_time['time'].values).month,
    'day': pd.to_datetime(data_loc_time['time'].values).day,
    'hour': pd.to_datetime(data_loc_time['time'].values).hour
    }
for i in range(len(datas)):
    variables[var[i]] = datas[i].values(lat, lon, dates, var[i])

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
    Z, T, P, pwv = amutils.profiles(paramsfile, T0, P0, PWV, m, N)
    amutils.config(freq_start, freq_stop, freq_interval, 2.7, Z, T, P, pwv, DIR+'/am/config/'+filename+date)
    file.write(filename+date+'\n')
file.close()
####################################
