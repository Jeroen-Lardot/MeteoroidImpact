from Environment import Environment
from Spacecraft import Spacecraft
from models.VELOCITY import VELOCITY
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
import os

# Load everything in
environment = Environment("models/spenvisdata.csv", VELOCITY.TAYLOR)
spacecraft = Spacecraft(environment)
masses = [mass * 0.001 for mass in environment.getMasses()][0:140]  # gives masses in kg
IndividualFluxes = [flux for flux in environment.getFluxes()][0:140]   # gives flux in 1/(m^2 * yr)
diameters = [diameter * 0.01 for diameter in environment.getDiameters()][0:140]   # gives diameters in m
densities = [density * 1000 for density in environment.getDensities()][0:140]   # gives densities in kg/m^-3
print(masses[139])
# Give specifications of the run
N = 10**2
materialType = 'TITANIUM' # CARBONFIBER / TITANIUM / ALUMINIUM
thickness = 0.3 # milimeter


# Get name where file is based
basename = 'run_{}_{}_{}'.format(N, materialType, thickness)
path = '../Simulation_data/' + basename

# Retrieve files and data
dataPerRun = pd.read_csv(path + '/' + 'dataPerRun.csv', header=0, sep='\t')
dataPerBin = pd.read_csv(path + '/' + 'dataPerBin.csv', header=0, sep='\t')
print(dataPerBin)

# Unpack all the data
A_tot, Perf_tot, Perf_area = dataPerRun["A_tot"], dataPerRun["Perf_tot"], dataPerRun["Perf_area"]
AA_MEAN, AA_STD, CRAT_MEAN, CRAT_STD = dataPerBin["AA_MEAN"], dataPerBin["AA_STD"],dataPerBin["CRAT_MEAN"], dataPerBin["CRAT_STD"]

# The average total damaged area and perforations + their standard deviation
A_MEAN = np.mean(A_tot)
A_STD = np.std(A_tot)
print(thickness)
print(r'Total damage = ${} \pm {}$'.format(A_MEAN, A_STD))

perf_MEAN = np.mean(Perf_tot)
perf_STD = np.std(Perf_tot)
print(r'Perforations = ${} \pm {}$'.format(perf_MEAN, perf_STD))
print(r'Perforation Area = ${} \pm {}$'.format(np.mean(Perf_area), np.std(Perf_area)))

# Make craterdepth-profile
depth_i, depth_f = [-3, -8]
CRAT_PROFILE = []
Depths = 10**np.linspace(depth_i,depth_f,1000)
for depth in Depths:
    i=0
    areaDamage = 0
    for craterDepth in CRAT_MEAN:
        if craterDepth > depth:
            areaDamage = areaDamage + AA_MEAN[i]
        i+=1
        
   # if thickness*10**-3 > depth:
        #areaDamage = areaDamage + np.mean(Perf_area)
    CRAT_PROFILE.append(areaDamage)


# Set directory where plots will appear
if not os.path.exists('../plots/'):
    os.mkdir('../plots/')
figDir = '../plots/' + basename
if not os.path.exists(figDir):
    os.mkdir(figDir)

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
    ax.scatter(np.log10(masses), AA_MEAN, s=10, color=plotColor, label='{}, Thickness = {} mm'.format(materialType.lower(), thickness))
    ax.errorbar(np.log10(masses), AA_MEAN, yerr = AA_STD, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
    ax.set_xlabel('$\log$ Masses (kg)', size= 15)
    ax.set_ylabel('Damaged area fraction', size= 15)
    ax.grid()

    ax.legend(fontsize= 10)
    figAA_MEAN.savefig(figDir + '/' + 'AA_MEAN.png', dpi= 400, bbox_inches= 'tight') 

# CRAT_MEAN
def Plot_CRAT_MEAN():
    figCRAT_MEAN, ax = plt.subplots()
    ax.scatter(masses, CRAT_MEAN, s=10, color=plotColor, label='{}, Thickness = {} mm'.format(materialType.lower(), thickness))
    ax.errorbar(masses, CRAT_MEAN, yerr = CRAT_STD, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
    ax.set_xlabel('Masses (kg)', size= 15)
    ax.set_ylabel('Craterdepth (m)', size= 15)
    ax.set_xscale('log')
    ax.grid()
    ax.legend(fontsize= 10)
    figCRAT_MEAN.savefig(figDir + '/' + 'CRAT_MEAN.png', dpi= 400, bbox_inches= 'tight') 

# Craterdepth profile
def Plot_CRAT_PROFILE():
    figCRAT_PROFILE, ax = plt.subplots()
    ax.scatter(Depths, CRAT_PROFILE, s=5, color=plotColor, label='{}, Thickness = {} mm'.format(materialType.lower(), thickness))
    #ax.errorbar(np.log10(masses), CRAT_MEAN, yerr = CRAT_STD, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
    ax.set_xlabel('Craterdepth (m)', size= 15)
    ax.set_ylabel('Cumulative damaged area fraction', size= 15)
    ax.set_xscale('log')
    #ax.set_yscale('log')

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
Plot_CRAT_PROFILE()
#Plot_Order_of_magnitude_picture()
#Plot_Flux()

plt.show()


