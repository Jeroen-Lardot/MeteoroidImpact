from Environment import Environment
from Spacecraft import Spacecraft
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
import os

from models.MATERIAL import MATERIAL

environment = Environment("models/spenvisdata.csv")
spacecraft = Spacecraft(MATERIAL.ALUMINIUM, 0.0003, environment)
masses = [mass * 0.001 for mass in environment.getMasses()][0:112]  # gives masses in kg
IndividualFluxes = [flux for flux in environment.getFluxes()][0:112]   # gives flux in 1/(m^2 * yr)
diameters = [diameter * 0.01 for diameter in environment.getDiameters()][0:112]   # gives diameters in m
densities = [density * 1000 for density in environment.getDensities()][0:112]   # gives densities in kg/m^-3
# Give specifications of the run
N = 10000
materialType = 'ALUMINIUM' # CARBONFIBER / TITANIUM / ALUMINIUM
thickness = 0.3 # milimeter

# Get name where file is based
basename1 = 'run_{}_{}_{}'.format(20000, 'TITANIUM', 0.3)
basename2 = 'run_{}_{}_{}'.format(20000, 'TITANIUM', 0.6)
basename3 = 'run_{}_{}_{}'.format(20000, 'TITANIUM', 1.0)
path1 = '../Simulation_data/' + basename1
path2 = '../Simulation_data/' + basename2
path3 = '../Simulation_data/' + basename3

# Retrieve files and data
dataPerBin1 = pd.read_csv(path1 + '/' + 'dataPerBin.csv', header=0, sep='\t')
dataPerBin2 = pd.read_csv(path2 + '/' + 'dataPerBin.csv', header=0, sep='\t')
dataPerBin3 = pd.read_csv(path3 + '/' + 'dataPerBin.csv', header=0, sep='\t')

# Unpack all the data
AA_MEAN1, AA_STD1, CRAT_MEAN1, CRAT_STD1 = dataPerBin1["AA_MEAN"], dataPerBin1["AA_STD"],dataPerBin1["CRAT_MEAN"], dataPerBin1["CRAT_STD"]
AA_MEAN2, AA_STD2, CRAT_MEAN2, CRAT_STD2 = dataPerBin2["AA_MEAN"], dataPerBin2["AA_STD"],dataPerBin2["CRAT_MEAN"], dataPerBin2["CRAT_STD"]
AA_MEAN3, AA_STD3, CRAT_MEAN3, CRAT_STD3 = dataPerBin3["AA_MEAN"], dataPerBin3["AA_STD"],dataPerBin3["CRAT_MEAN"], dataPerBin3["CRAT_STD"]

# Define plotting choices
plotColor = 'steelblue'

errorColor = 'darkslategrey'
errorThickness = 0.5
errorCapsize = 0.5

plt.style.use("default")
# Plot flux

# AA_MEAN
def Plot_AA_MEAN():
    figAA_MEAN, ax = plt.subplots()

    ax.scatter(np.log10(masses), AA_MEAN1, s=20, color='steelblue', marker="v", label='{}, Thickness = {} mm'.format('TITANIUM', 0.3))
    ax.plot(np.log10(masses), AA_MEAN1, color='steelblue',alpha=0.4)
    #ax.errorbar(np.log10(masses), AA_MEAN1, yerr = AA_STD1, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(np.log10(masses), AA_MEAN2, s=20, color="r",marker='x', label='{}, Thickness = {} mm'.format('TITANIUM', 0.6))
    ax.plot(np.log10(masses), AA_MEAN2, color='r',alpha=0.4)
    #ax.errorbar(np.log10(masses), AA_MEAN2, yerr = AA_STD2, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(np.log10(masses), AA_MEAN3, s=20, color="y", label='{}, Thickness = {} mm'.format('TITANIUM', 1.0))
    ax.plot(np.log10(masses), AA_MEAN3, color='y',alpha=0.4)
    ax.errorbar(np.log10(masses), AA_MEAN3, yerr = AA_STD3, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
    plt.ylim(0,8*10**-7)
    ax.set_xlabel('$\log$ Masses (kg)', size= 15)
    ax.set_ylabel('Damaged area fraction', size= 15)
    #ax.set_xscale('log')
    ax.grid()
    ax.legend(fontsize= 10)

# CRAT_MEAN
def Plot_CRAT_MEAN():
    figCRAT_MEAN, ax = plt.subplots()

    ax.scatter(masses, np.log10(CRAT_MEAN1), s=20, color='steelblue', marker="v", label='{}, Thickness = {} mm'.format('TITANIUM', 0.3))
    ax.plot(masses, np.log10(CRAT_MEAN1), color='steelblue',alpha=0.4)
    ax.errorbar(masses, np.log10(CRAT_MEAN1), yerr = CRAT_STD1, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(masses, np.log10(CRAT_MEAN2), s=20, color='r', marker="x", label='{}, Thickness = {} mm'.format('TITANIUM', 0.6))
    ax.plot(masses, np.log10(CRAT_MEAN2), color='r',alpha=0.4)
    ax.errorbar(masses, np.log10(CRAT_MEAN2), yerr = CRAT_STD2, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(masses, np.log10(CRAT_MEAN3), s=20, color='y', label='{}, Thickness = {} mm'.format('TITANIUM', 1.0))
    ax.plot(masses, np.log10(CRAT_MEAN3), color='y',alpha=0.4)
    ax.errorbar(masses, np.log10(CRAT_MEAN3), yerr = CRAT_STD3, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")


    ax.set_xlabel('Masses (kg)', size= 15)
    ax.set_ylabel('(log) Craterdepth (m)', size= 15)
    ax.set_xscale('log')
    ax.grid()
    ax.legend(fontsize= 10)

# Craterdepth profile
def Plot_CRAT_PROFILE():
    figCRAT_PROFILE, ax = plt.subplots()
    ax.scatter(Depths, CRAT_PROFILE, s=5, color=plotColor, label='{}, Thickness = {} mm'.format(materialType.lower(), thickness))
    #ax.errorbar(np.log10(masses), CRAT_MEAN, yerr = CRAT_STD, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
    ax.set_xlabel('Craterdepth (m)', size= 15)
    ax.set_ylabel('Cumulative damaged area fraction', size= 15)
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.grid()
    ax.legend(fontsize= 10)
    figCRAT_PROFILE.savefig(figDir + '/' + 'CRAT_PROFILE.png', dpi= 400, bbox_inches= 'tight')

# Rough Order of magnitude approx
def Plot_Order_of_magnitude_picture():
    Rough_damaged_area = np.pi*(np.array(diameters)*(1/2))**2
    expDamage = Rough_damaged_area*IndividualFluxes

    figORDER_OM, ax = plt.subplots()
    ax.scatter(masses, expDamage, s=5, color=plotColor)
    ax.set_xlabel('Masses (kg)', size= 15)
    ax.set_ylabel('Damaged area fraction', size= 15)
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.grid()
    #ax.legend(fontsize= 10)
    figORDER_OM.savefig(figDir + '/' + 'ORDER_OM.png', dpi= 400, bbox_inches= 'tight')

def Plot_Flux():
    figFLUX, ax = plt.subplots()
    ax.scatter(masses, IndividualFluxes, s=5, color=plotColor)
    ax.set_xlabel('Masses (kg)', size= 15)
    ax.set_ylabel('Flux $(1/ yr \, m^2)$', size= 15)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid()
    #ax.legend(fontsize= 10)
    figFLUX.savefig(figDir + '/' + 'FLUX.png', dpi= 400, bbox_inches= 'tight')



#PLOTTING

Plot_AA_MEAN()
Plot_CRAT_MEAN()
#Plot_CRAT_PROFILE()
#Plot_Order_of_magnitude_picture()
#Plot_Flux()

plt.show()