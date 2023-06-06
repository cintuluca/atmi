##
# @file src/vprofiles.py
# @brief Singular realization am configuration file writer.
#
# Python script necessary to calculate the vertical profiles of the atmospheric parameters and write the am configuration file for a given single realization of the atmosphere.
#
# The file is located under atmi/src.

from lib import amutils
import os
import sys

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
T0, P0, PWV, month, N, freq_start, freq_stop, freq_interval, filename, paramsfile = args

print('Atmospheric Temperature\t->\t', T0, 'K')
print('Atmospheric Pressure\t->\t', P0, 'Pa')
print('Atmospheric PWV\t\t->\t', PWV, 'mm')
print('Month\t\t\t', month)
print('Number of Layers\t->\t', N)
print('Starting Frequency\t->\t', freq_start, 'GHz')
print('Ending Frequency\t->\t', freq_stop, 'GHz')
print('Frequency Interval\t->\t', freq_interval, 'GHz')
print('Filename\t\t->\t', filename)
print('Parameters File\t->\t', paramsfile)

T0, P0, PWV, month, N, freq_start, freq_stop, freq_interval = [float(T0), float(P0), float(PWV), int(month), int(N), float(freq_start), float(freq_stop), float(freq_interval)]
#################################

## Calculating the vertical profiles
####################################
Z, T, P, pwv = amutils.profiles(paramsfile, T0, P0, PWV, month, N)
####################################

## Saving the am configuration file
####################################
amutils.config(freq_start, freq_stop, freq_interval, 2.7, Z, T, P, pwv, DIR+'/am/config/'+filename)
print('am configuration file saved in '+DIR'/am/config/'+filename+'.amc!')
####################################
