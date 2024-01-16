## @file src/amconfig.py
# @brief Generator of the am configuration file.
#
# Python script necessary to calculate the vertical profiles of the atmospheric parameters and write the am configuration file.
#
# The file is located under atmi/src.

from lib import amutils
import os
import pandas as pd
import sys
from tqdm import tqdm

with open(os.path.expanduser('~')+'/.atmi') as file:
    DIR = file.readline().strip('\n')   # Global path of the project

## Reading the configuration file
#################################
config = sys.argv[1]
if os.path.exists(config) == False:
	print('Directory not found!')
	sys.exit()
	
with open(config) as f:
	args = f.readlines()
	args = [arg.rstrip('\n') for arg in args]
samplingfile, N, freq_start, freq_stop, freq_interval, paramsfile, filename = args

print('Sampling File\t->\t', samplingfile)
print('Number of Layers\t->\t', N)
print('Starting Frequency\t->\t', freq_start, 'GHz')
print('Ending Frequency\t->\t', freq_stop, 'GHz')
print('Frequency Interval\t->\t', freq_interval, 'GHz')
print('Parameters File\t->\t', paramsfile)
print('Filename\t\t->\t', filename)

N, freq_start, freq_stop, freq_interval = [int(N), float(freq_start), float(freq_stop), float(freq_interval)]
#################################

## Saving all the configuration files
#####################################
df = pd.read_csv(samplingfile, header=1, names=['Month', 'Day', 'Hour', 'T', 'P', 'PWV'])

file = open(DIR+'/am/config/'+filename+'.txt', 'w')
print('\nSaving the configuration files in '+DIR+'/am/config/ ...')
for i in tqdm(range(len(df.index)), desc='Loading ...'):

    m, d, h = str(int(df.iloc[i]['Month'])), str(int(df.iloc[i]['Day'])), str(int(df.iloc[i]['Hour']))
    if len(m) == 1:
        m = '0'+m
    if len(d) == 1:
        d = '0'+d
    if len(h) == 1:
        h = '0'+h
    date = m+d+h

    T0, P0, PWV = df.iloc[i]['T'], df.iloc[i]['P'], df.iloc[i]['PWV']
    Z, T, P, pwv = amutils.profiles(paramsfile, T0, P0, PWV, int(m), N)
    amutils.config(freq_start, freq_stop, freq_interval, 2.7, Z, T, P, pwv, DIR+'/am/config/'+filename+date)
    file.write(filename+date+'\n')
file.close()
####################################
