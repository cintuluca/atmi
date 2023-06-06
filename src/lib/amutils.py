"""! @brief Gathers some useful functions for am usage."""
##
# @file src/lib/amutils.py
# @brief File for the lib.amutils package.
#
# The file is located under atmi/src/lib.
#
# @package lib.amutils
# @brief Gathers some useful functions for am usage.
#
# @section description_amutils Description
# Defines the functions necessary to calculate the vertical profiles and to write and save the am configuration files.
# - profiles (function)
# - config (function)
# - am_plot (function)
#
# @section libraries_amutils Libraries/Modules
# - datetime standard library (https://docs.python.org/3/library/datetime.html)
#   - Access to datetime function.
# - matplotlib.pyplot (https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
#   - Access to plot functions.
# - numpy (https://numpy.org/doc/stable/)
#   - Access to many useful functions for array manipulation.
# - pandas (https://pandas.pydata.org/docs/reference/index.html)
#   - Access to read_table function.
#
# @section notes_amutils Notes
# - Comments are Doxygen compatible.
#
# @section todo_amutils TODO
# - None.
#
# @section author_amutils Author(s)
# - Created by Luca Cintura on 20/03/2023.
# - Modified by Luca Cintura on 20/03/2023.

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## This function calculates the value of the temperature, pressure and PWV through 30 Km of atmosphere using vertical profiles functions.
#
#  @param paramsfile The path for the parameters file.
#  @param T0 The temperature at surface.
#  @param P0 The pressure at surface.
#  @param PWV The PWV of the atmosphere column.
#  @param month The month, in order to chose the correct vertical profiles.
#  @param N The number of layers for the atmosphere discretization.
def profiles(paramsfile, T0, P0, PWV, month, N):
	params = np.loadtxt(paramsfile, skiprows=4)
	Ht, a1, a2, b1, b2, Hp, Hw, hT0, hP0, hW0, hsite = params[int(month-1)]
	Z = hsite + np.linspace(0, 30, num=N)
	T0 = T0 - a1*hT0**2 - b1*hT0**2
	P0 = P0*np.exp(hP0/Hp)
	PWV0 = np.abs(PWV)/np.sum(np.exp(-(Z-hsite)/Hw))
	PWV0 = PWV0*np.exp(hW0/Hw)
	c2 = a1*Ht**2+b1*Ht+T0
	T1 = a1*Z**2+b1*Z+T0
	T2 = a2*(Z-Ht)**2+b2*(Z-Ht)+c2
	T = np.concatenate((T1[np.where(Z<Ht)[0]], T2[np.where(Z>=Ht)[0]]))
	P = P0*np.exp(-Z/Hp)
	pwv = PWV0*np.exp(-Z/Hw)
	return Z, T, P, pwv

## This function creates the configuration file to run am.
#
#  @param freq_start The starting frequency.
#  @param freq_stop The ending frequency.
#  @param freq_interval The frequency interval for am simulation.
#  @param T0 The background temperature.
#  @param Z The index for each one of the atmospheric layers.
#  @param T The temperature for each one of the atmospheric layers.
#  @param P The pressure for each one of the atmospheric layers.
#  @param pwv The PWV for each one of the atmospheric layers.
#  @param filename The path for the configuration file.
def config(freq_start, freq_stop, freq_interval, T0, Z, T, P, pwv, filename):
	file = open(filename+'.amc', 'w')
	file.write('# '+str(datetime.now())+'\n\n')
	file.write('f '+str(freq_start)+' GHz '+str(freq_stop)+' GHz '+str(freq_interval)+' GHz\n\n')
	file.write('T0 '+str(T0)+' K\n\n')
	for i in range(len(Z)):
		j = len(Z)-i-1
		file.write('layer\n')
		file.write('Pbase '+str(P[j])+' Pa\t# z = '+str(Z[j])+' Km\n')
		file.write('Tbase '+str(T[j])+' K\n')
		file.write('column dry_air vmr\n')
		file.write('column h2o '+str(pwv[j])+' mm_pwv\n\n')
	file.close()
	
## This function plots the resulting brightness temperatures resulting from am.
#
#  @param output_file The path to the am output file.
def am_plot(output_file):
	atm = pd.read_table(output_file, names=['Freq', 'Line', 'Tb'], sep=' ')
	plt.plot(atm['Freq'], atm['Tb'])
	plt.xlim(atm['Freq'].min(), atm['Freq'].max())
	plt.ylim(0, atm['Tb'].max()+10)
	plt.grid()
	plt.xlabel('Frequency [GHz]')
	plt.ylabel(r'$T_{atm} [K_{RJ}]$')
	plt.xticks(np.arange(atm['Freq'].min(),atm['Freq'].max()+1,10))
	plt.yticks(np.arange(0,atm['Tb'].max()+10,25))
	plt.show()
