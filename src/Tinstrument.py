## @file src/Tinstrument.py
# @brief Takes into account the characteristics of the instrument observing the sky.
#
# Python script necessary to perform the frequency band integration and the beam pattern convolution.
#
# The file is located under atmi/src.

from lib import instrumentObs
from datetime import datetime
import numpy as np
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
spectrumfile, theta0, FWHM, freq1, freq2 = args

print('Spectrum File\t\t->\t', spectrumfile)
print('Theta Pointing\t\t->\t', theta0+'°')
print('Antenna FWHM\t\t->\t', FWHM+'°')
print('Starting Frequency\t->\t', freq1, 'GHz')
print('Ending Frequency\t->\t', freq2, 'GHz')

theta0, FWHM, freq1, freq2 = [float(theta0), float(FWHM), float(freq1), float(freq2)]
#################################

## Setting up the characteristics of the instrument
###################################################
theta1, theta2 = theta0-5*FWHM, theta0+5*FWHM
theta = np.linspace(theta1, theta2, 100)

files = []
for file in os.listdir(DIR+'/am/output'):
    if file.startswith(spectrumfile):
        if file.replace(spectrumfile, '').replace('.out', '').isnumeric():
            files.append(file)
        
print('\nCalculating the measurements of the instrument\t...')
Tatm, m, d, h = [], [], [], []
for i in tqdm(range(len(files)), desc='Loading ...'):
    file = files[i]
    df = pd.read_table(DIR+'/am/output/'+file, names=['Freq', 'Abs', 'Tb'], sep=' ')
    T = np.array(df[(df['Freq'] >= freq1) & (df['Freq'] <= freq2)]['Tb'])
    freq = np.array(df[(df['Freq'] >= freq1) & (df['Freq'] <= freq2)]['Freq'])
    alpha = np.array(df[(df['Freq'] >= freq1) & (df['Freq'] <= freq2)]['Abs'])
    
    band = np.zeros(len(freq)) + 1 # top-hat
    Pn = instrumentObs.Pn_gaussian(theta, theta0, FWHM)    # gaussian normalized antenna pattern
    obs = instrumentObs.instrument(theta, Pn, freq, band)
    Tatm.append(obs.observation(T - 2.7*alpha))
    mdh = file.replace(spectrumfile, '').replace('.out', '')
    m.append(mdh[0:2]), d.append(mdh[2:4]), h.append(mdh[4:6]) 
    
###################################################

## Saving the results on a .csv file
####################################   
df = pd.DataFrame(Tatm, columns=['Tatm'])
df.insert(0, 'Month', m), df.insert(1, 'Day', d), df.insert(2, 'Hour', h)

if os.path.exists(DIR+'/outputs/instrument/'+spectrumfile+'.csv') == True:
	with open(DIR+'/outputs/instrument/'+spectrumfile+'.csv', 'r+') as f:
	    f.truncate(0)

with open(DIR+'/outputs/instrument/'+spectrumfile+'.csv', 'a') as f:
	f.write('# '+str(datetime.now())+'\n\n')
	df.to_csv(f, index=False)
    
print('Results saved in '+DIR+'/outputs/instrument/'+spectrumfile+'.csv!')
####################################
