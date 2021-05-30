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


# Give specifications of the run
N = 1000
materialType = 'ALUMINIUM' # CARBONFIBER / TITANIUM / ALUMINIUM
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

perf_MEAN = np.mean(Perf_tot)
perf_STD = np.std(Perf_tot)

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

# Plot AA_MEAN
figAA_MEAN, ax = plt.subplots()
ax.scatter(np.log10(masses), AA_MEAN, s=10, color=plotColor, label='{}, thickness = {} mm'.format(materialType.lower(), thickness))
ax.errorbar(np.log10(masses), AA_MEAN, yerr = AA_STD, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
ax.set_xlabel('$\log$ masses (kg)', size= 15)
ax.set_ylabel('Damaged area fraction', size= 15)
ax.grid()
ax.legend(fontsize= 10)
figAA_MEAN.savefig(figDir + '/' + 'AA_MEAN.png', dpi= 400, bbox_inches= 'tight') 

# Plot CRAT_MEAN
figCRAT_MEAN, ax = plt.subplots()
#ax.plot(np.log10(masses), CRAT_MEAN ,"b-", label='{}, thickness = {} mm'.format(materialType.lower(), thickness))
ax.scatter(np.log10(masses), CRAT_MEAN, s=10, color=plotColor, label='{}, thickness = {} mm'.format(materialType.lower(), thickness))
ax.errorbar(np.log10(masses), CRAT_MEAN, yerr = CRAT_STD, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
ax.set_xlabel('$\log$ masses (kg)', size= 15)
ax.set_ylabel('Craterdepth (m)', size= 15)
ax.grid()
ax.legend(fontsize= 10)

figCRAT_MEAN.savefig(figDir + '/' + 'CRAT_MEAN.png', dpi= 400, bbox_inches= 'tight') 


plt.show()


