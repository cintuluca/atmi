## @file src/amplot.py
# @brief Draws the plot of the am output file.
#
# Python script that plots the atmospheric brightness temperature spectrum resulting from the am simulation.
#
# The file is located under atmi/src.

from lib import amutils
import os
import sys

with open(os.path.expanduser('~')+'/.atmi') as file:
    DIR = file.readline().strip('\n')   # Global path of the project

filename = sys.argv[1]
print('Plotting on canvas the results ...')
amutils.am_plot(DIR+'/am/output/'+filename+'.out')
