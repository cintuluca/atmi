## @file src/pdfplot.py
# @brief Draws the plot of the pdf for the given variable.
#
# Python script that plots the probability density function associated with an atmospheric variable at the given time of the year (month/day/hour).
#
# The file is located under atmi/src.

from lib import atmsampling
from lib import netCDFutils
import numpy as np
import os
import pandas as pd
import sys
import xarray as xr

## Reading the configuration file
#################################
config = sys.argv[1]
if os.path.exists(config) == False:
	print('Directory not found!')
	sys.exit()

with open(config) as f:
	args = f.readlines()
	args = [arg.rstrip('\n') for arg in args]
datafile, var, month, day, hour, lat, lon, plot = args

print('Datafile\t->\t'+datafile)
if os.path.exists(datafile) == False:
	print('Directory not found!')
	sys.exit()
	
data = netCDFutils.data(datafile)   # opening dataset
names = data.variables()

print('Varible\t\t->\t'+var)
if names.count(var) == 0:
	print('Variable name not valid!')
	sys.exit()
	
print('Month\t\t->\t'+month)
if (float(month) != int(month)) & (float(month) <= 0) & (float(month) > 12):
	print('Month not valid!')
	sys.exit()

days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
print('Day\t\t->\t'+day)
if (float(day) != int(day)) & (float(day) <= 0) & (float(day) > days[int(month)-1]):
        print('Day not valid!\n')
        sys.exit()

print('Hour\t\t->\t'+hour)
if (float(hour) != int(hour)) & (float(hour) < 0) & (float(hour) > 23):
        print('Hour not valid!\n')
        sys.exit()

print('Latitude\t->\t'+lat)
print('Longitude\t->\t'+lon)
lat, lon = [float(lat), float(lon)]
#################################

## Calculating the pdf
######################
window = netCDFutils.window(data.start + 1, data.stop - 1, month, day, hour, 4)
values = data.values(lat, lon, window, var)
variable = atmsampling.variable(var, values)
######################

## Plotting the pdf
###################
if plot == 'term':
	print('\nPlotting on a terminal ...\n')
	variable.termplot_pdf()
	print('')
elif plot == 'canvas':
	print('\nPlotting on a canvas ...\n')
	variable.plot_pdf()
else:
	print('Plot option not valid!')
	sys.exit()
###################
