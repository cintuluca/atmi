"""! @brief Gathers some useful functions for netCDF data manipulation."""
##
# @file src/lib/netCDFutils.py
# @brief File for the lib.netCDFutils package.
#
# The file is located under atmi/src/lib.
#
# @package lib.netCDFutils
# @brief Gathers some useful functions for netCDF data manipulation.
#
# @section description_netCDFutils Description
# Defines the user class for the manipulation of generic netCDF dataset and a function for time dates selection.
# - data (class)
# - window (function)
#
# @section libraries_netCDFutils Libraries/Modules
# - numpy (https://numpy.org/doc/stable/)
#   - Access to many useful functions for array manipulation.
#   - Access to datetime64 and timedelta64.
# - xarray (https://docs.xarray.dev/en/stable/)
#   - Access to netCDF dataset manipulation functions.
# - pandas (https://pandas.pydata.org/docs/reference/index.html)
#   - Access to to_datetime class.
#
# @section notes_netCDFutils Notes
# - Comments are Doxygen compatible.
#
# @section todo_netCDFutils TODO
# - None.
#
# @section author_netCDFutils Author(s)
# - Created by Luca Cintura on 20/03/2023.
# - Modified by Luca Cintura on 20/03/2023.

import numpy as np
import pandas as pd
import xarray as xr

## This function gives the days in a window of some days around a specific date.
#
#  @param start The starting year.
#  @param stop The final year.
#  @param month The month of the specific date.
#  @param day The day of the specific date.
#  @param hour The hour of the specific date.
#  @param interval The number of days of the semi-window.
def window(start, stop, month, day, hour, interval):
	years = np.arange(start, stop+1, 1)
	days = np.arange(-interval, interval+1, 1)
	W = []
	for year in years:
		d0 = np.datetime64(str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour))
		for d in days:
			W.append(d0 + np.timedelta64(d, 'D').astype('timedelta64[h]'))
	return W
	
## This class gathers some xarray utility tools.
#
#  More details.
class data:

    ## The constructor for the class.
    #
    #  @param self The object pointer.
    #  @param datafile The path to the netCDF dataset.
    def __init__(self, datafile):
        ## The dataset containing the data.
        self.dataset = xr.open_dataset(datafile)
        ## The starting year of the dataset.
        self.start = pd.to_datetime(np.array(self.dataset['time'][0])).year
        ## The final year of the dataset.
        self.stop = pd.to_datetime(np.array(self.dataset['time'][-1])).year
      
    ## This method gives the name of all the variables of the dataset.
    #
    #  @param self The object pointer.
    def variables(self):
        return list(self.dataset.keys())
	
    ## This method gives the units for all the variables of the dataset.
    #
    #  @param self The object pointer.
    def units(self):
        return list(self.dataset[v].attrs['units'] for v in self.variables())

    ## This method gives filters the dataset values through a days window, at fixed coordinates (latitude, longitude).
    #
    #  @param self The object pointer.
    #  @param latitude The fixed latitude.
    #  @param longitude The fixed longitude.
    #  @param window The days window to filter the data.
    #  @param name The name of the desired variable.
    def values(self, latitude, longitude, window, name):
        data = self.dataset
        if list(data.coords).count('expver') != 0:
            data = data.sel(expver=1)
        data = data.sortby(data['time'])
        data_loc_time = data.sel(time=window, longitude=longitude, latitude=latitude, method='nearest')
        return np.ma.masked_invalid(data_loc_time[name].values)
