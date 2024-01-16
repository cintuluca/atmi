"""! @brief Gathers some useful functions for the computation of the instrument observation."""
##
# @file src/lib/instrumentObs.py
# @brief File for the lib.instrumentObs package.
#
# The file is located under atmi/src/lib.
#
# @package lib.instrumentObs
# @brief Gathers some useful functions for the computation of the instrument observation.
#
# @section description_instrumentObs Description
# Defines the instrument class for the computation of the antenna temperature and frequency band integration.
# - instrument (class)
# - azimuth (function)
# - Tazimuth (function)
# - Pn_gaussian (function)
#
# @section libraries_instrumentObs Libraries/Modules
# - numpy (https://numpy.org/doc/stable/)
#   - Access to many useful functions for array manipulation.
# - scipy.stats (https://docs.scipy.org/doc/scipy/reference/stats.html)
#   - Access to multivariate_normal function.
#
# @section notes_instrumentObs Notes
# - Comments are Doxygen compatible.
#
# @section todo_instrumentObs TODO
# - None.
#
# @section author_instrumentObs Author(s)
# - Created by Luca Cintura on 10/05/2023.
# - Modified by Luca Cintura on 10/05/2023.

import numpy as np
import scipy.stats as st

## This function calculates the atmospheric variable depending on the azimuth.
#
#  @param T0 The brightness temperature at the azimuth.
#  @param theta The azimuth angle.
def Tazimuth(T0, theta):
    theta = theta*np.pi/180
    return T0/np.cos(theta)

## This function calculates the normalized gaussian pattern of the antenna.
#
#  @param theta The azimuth angles.
#  @param mean The pointing of the antenna.
#  @param FWHM The FWHM of the antenna.
def Pn_gaussian(theta, mean, FWHM):
    gaussian = st.multivariate_normal(mean, FWHM/(2*np.sqrt(2*np.log(2))))
    return gaussian.pdf(theta)/gaussian.pdf(mean)
    
## This class can consider the instrument characteristics for the observation.
#
#  More details.
class instrument:

    ## The constructor for the class.
    #
    #  @param self The object pointer.
    #  @param theta The azimuth angles.
    #  @param Pn The normalized pattern of the antenna.
    #  @param freq The considered frequencies.
    #  @param band The band function of the instrument.
    def __init__(self, theta, Pn, freq, band):
        self.pattern = {'theta':theta, 'Pn':Pn}
        self.fband = {'freq':freq, 'band':band}

    ## This method calculates the antenna temperature for a given brightness temperature at the azimuth.
    #
    #  @param self The object pointer.
    #  @param T0 The brightness temperature at the azimuth.
    def Tantenna(self, T0):
        theta, Pn = self.pattern['theta'], self.pattern['Pn']
        Tb = Tazimuth(T0, theta)
        A1, A2 = 0, 0
        for i in range(len(Pn)-1):
            A1 = A1 + np.mean(Tb[i:i+2]) * np.mean(Pn[i:i+2]) * (theta[i+1] - theta[i])
            A2 = A2 + np.mean(Pn[i:i+2]) * (theta[i+1] - theta[i])
        return A1/A2

    ## This method integrates in the band function of the isntrument.
    #
    #  @param self The object pointer.
    #  @param Ta The antenna temperature at the frequencies of the instrument.
    def bandinteg(self, Ta):
        freq, band = self.fband['freq'], self.fband['band']
        A1, A2 = 0, 0
        for i in range(len(freq)-1):
            A1 = A1 + np.mean(Ta[i:i+2]) * np.mean(band[i:i+2]) * (freq[i+1] - freq[i])
            A2 = A2 + np.mean(band[i:i+2]) * (freq[i+1] - freq[i])
        return A1/A2

    ## This method calculates the antenna temperature for a given brightness temperature at the azimuth.
    #
    #  @param self The object pointer.
    #  @param T0 The brightness temperature at the azimuth.
    def observation(self, T0):
        Ta = []
        for T in T0:
            Ta.append(self.Tantenna(T))
        return self.bandinteg(Ta)
