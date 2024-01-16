"""! @brief Defines some useful classes for atmosphere sampling."""
##
# @file src/lib/atmsampling.py
# @brief File for the lib.atmsampling package.
#
# The file is located under atmi/src/lib.
#
# @package lib.atmsampling
# @brief Defines some useful classes for atmosphere sampling.
#
# @section description_atmsampling Description
# Defines the base and end user classes for the sampling of generic atmosphere's realizations.
# - variable (base class)
# - atmosphere
# - sampling
#
# @section libraries_atmsampling Libraries/Modules
# - matplotlib.pyplot (https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
#   - Access to plot functions.
# - numpy (https://numpy.org/doc/stable/)
#   - Access to many useful functions for array manipulation.
# - scipy.linalg (https://docs.scipy.org/doc/scipy/reference/linalg.html)
#   - Access to eigh function, for the eigenvalues and eigenvectors determination.
# - scipy.stats (https://docs.scipy.org/doc/scipy/reference/stats.html) 
#   - Access to gaussian_kde function.
#   - Access to norm function.
# - termplotlib (https://pypi.org/project/termplotlib/)
#   - Access to terminal plot functions.
#
# @section notes_atmsampling Notes
# - Comments are Doxygen compatible.
#
# @section todo_atmsampling TODO
# - None.
#
# @section author_atmsampling Author(s)
# - Created by Luca Cintura on 20/03/2023.
# - Modified by Luca Cintura on 20/03/2023.

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh
from scipy.stats import gaussian_kde, norm
import termplotlib as tpl
	
## This class represents the generic atmospheric variable.
#
#  More details.
class variable:

    ## The constructor for the class.
    #
    #  @param self The object pointer.
    #  @param name The name of the variable.
    #  @param values The values assumed by the variable.
    def __init__(self, name, values):
        ## The name of the variable.
        self.name = name
        ## The values defining the variable statistics.
        self.values = np.ma.masked_invalid(values)
        ## The probability density function calculated using KDE.
        self.pdf = gaussian_kde(self.values) 
     
    ## This method samples one value for the variable, using his pdf.
    #
    #  @param self The object pointer.
    #  @param N The number of desired samplings.
    def sample(self, N):
        return self.pdf.resample(N)[0]
        
    ## This method plots the variable pdf on a canvas.
    #
    #  @param self The object pointer.
    def plot_pdf(self):
        x = np.linspace(self.values.min(), self.values.max(), 1000)
        y = self.pdf(x)
        plt.plot(x, y, c='r')
        plt.xlabel(self.name)
        plt.ylabel('PDF')
        plt.show()
      
    ## This method plots the variable pdf over the terminal.
    #
    #  @param self The object pointer.
    def termplot_pdf(self):
        x = np.linspace(self.values.min(), self.values.max(), 1000)
        y = self.pdf(x)
        fig = tpl.figure()
        fig.plot(x, y, width=60, height=20)
        fig.show()
      
## This class represents a specific realization of the atmosphere.
#
#  More details.
class atmosphere:
    
    ## The constructor for the class.
    #
    #  @param self The object pointer.
    #  @param variables The variables for the atmospheric realization.
    def __init__(self, variables):
        ## The variables defining the atmosphere realization.
        self.variables = variables
        ## The name of each variable.
        self.names = [var.name for var in variables]
        ## The values for each variable.
        self.values = np.array([var.values for var in variables])
        ## The mean value for each variable.
        self.means = np.array([np.mean(var.values) for var in variables])
        ## The standard deviation for each variable.
        self.stdevs = np.array([np.std(var.values) for var in variables])
        
    ## This method samples one value for each one of the variables, using their pdf.
    #
    #  @param self The object pointer.
    #  @param N The number of desired samplings.
    def sample(self, N):
        atm = []
        for var in self.variables:
            atm.append(var.sample(N))
        return np.array(atm).T
        
    ## This method calculates the covariance matrix for all the variables.
    #
    #  @param self The object pointer.
    def covariance(self):
        return np.cov(self.values)
  
## This class gathers more sequential realizations of the atmosphere.
#
#  More details.
class samplings:

    ## The constructor for the class.
    #
    #  @param self The object pointer.
    #  @param atmospheres The different realizations describing the atmosphere.
    def __init__(self, atmospheres):
        ## The different realizations describing the atmosphere.
        self.atmospheres = atmospheres
        ## The values for each variable of each realization.
        self.values = np.array([atm.values for atm in atmospheres])
     
    ## This method samples indipendently one realization for each one of the atmospheres, using the pdfs of their variables.
    #
    #  @param self The object pointer.
    #  @param N The number of desired samplings.
    def sample(self, N):
        sample = []
        for atm in self.atmospheres:
            sample.append(atm.sample(N))
        return np.array(sample)
     
    ## This method calculates the covariance matrix for all the variables.
    #
    #  @param self The object pointer.
    def covariance(self):
        a, b, c = np.shape(self.values)
        return np.cov(np.reshape((self.values), (a*b, c)))
        
    ## This method calculates the copula matrix.
    #
    #  @param self The object pointer.
    def copula(self):
        cov = self.covariance()
        evals, evecs = eigh(cov)
        return np.matmul(evecs, np.diag(np.sqrt(evals.clip(min=0))))
      
    ## This method samples one realization for each one of the atmospheres, inducing the correlations. It assumes gaussian probability.
    #
    #  @param self The object pointer.
    #  @param N The number of desired samplings.
    def correlated_sample_gaussian(self, N):
        nvar = np.sum([len(atmosphere.variables) for atmosphere in self.atmospheres])
        natm = len(self.atmospheres)
        means = np.reshape(np.array([atmosphere.means for atmosphere in self.atmospheres]), (nvar, 1))
        sample = norm.rvs(size = (nvar, N))
        C = self.copula()
        sampling = (np.dot(C, sample) + means).T
        a, b = np.shape(sampling)
        return np.reshape(sampling, (a, natm, b//natm))
        
    ## This method samples one realization for each one of the atmospheres, inducing the correlations. It not assumes gaussian probability.
    #
    #  @param self The object pointer.
    #  @param N The number of desired samplings.
    def correlated_sample(self, N):
        nvar = np.sum([len(atmosphere.variables) for atmosphere in self.atmospheres])
        natm = len(self.atmospheres)
        means = np.reshape(np.array([atmosphere.means for atmosphere in self.atmospheres]), (nvar, 1))
        stds = np.reshape(np.array([atmosphere.stdevs for atmosphere in self.atmospheres]), (nvar, 1))
        sample = np.array([s.T for s in self.sample(N)])
        a, b, c = np.shape(sample)
        sample = (np.reshape(sample, (a*b, c)) - means)/stds
        C = self.copula()
        sampling = (np.dot(C, sample) + means).T
        a, b = np.shape(sampling)
        return np.reshape(sampling, (a, natm, b//natm))
