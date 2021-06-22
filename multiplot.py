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
N = 20000
materialType = 'CARBONFIBER' # CARBONFIBER / TITANIUM / ALUMINIUM

# Get name where file is based
thickness1 = 0.3
thickness2 = 0.6
thickness3 = 1.0

basename1 = 'run_{}_{}_{}'.format(N, materialType, thickness1)
basename2 = 'run_{}_{}_{}'.format(N, materialType, thickness2)
basename3 = 'run_{}_{}_{}'.format(N, materialType, thickness3)
path1 = '../Simulation_data/' + basename1
path2 = '../Simulation_data/' + basename2
path3 = '../Simulation_data/' + basename3

# Retrieve files and data
dataPerBin1 = pd.read_csv(path1 + '/' + 'dataPerBin.csv', header=0, sep='\t')
dataPerBin2 = pd.read_csv(path2 + '/' + 'dataPerBin.csv', header=0, sep='\t')
dataPerBin3 = pd.read_csv(path3 + '/' + 'dataPerBin.csv', header=0, sep='\t')

dataPerRun1 = pd.read_csv(path1 + '/' + 'dataPerRun.csv', header=0, sep='\t')
dataPerRun2 = pd.read_csv(path2 + '/' + 'dataPerRun.csv', header=0, sep='\t')
dataPerRun3 = pd.read_csv(path3 + '/' + 'dataPerRun.csv', header=0, sep='\t')

# Unpack all the data
AA_MEAN1, AA_STD1, CRAT_MEAN1, CRAT_STD1 = dataPerBin1["AA_MEAN"], dataPerBin1["AA_STD"],dataPerBin1["CRAT_MEAN"], dataPerBin1["CRAT_STD"]
AA_MEAN2, AA_STD2, CRAT_MEAN2, CRAT_STD2 = dataPerBin2["AA_MEAN"], dataPerBin2["AA_STD"],dataPerBin2["CRAT_MEAN"], dataPerBin2["CRAT_STD"]
AA_MEAN3, AA_STD3, CRAT_MEAN3, CRAT_STD3 = dataPerBin3["AA_MEAN"], dataPerBin3["AA_STD"],dataPerBin3["CRAT_MEAN"], dataPerBin3["CRAT_STD"]

A_tot1, Perf_tot1, Perf_area1 = dataPerRun1["A_tot"], dataPerRun1["Perf_tot"], dataPerRun1["Perf_area"]
A_tot2, Perf_tot2, Perf_area2 = dataPerRun2["A_tot"], dataPerRun2["Perf_tot"], dataPerRun2["Perf_area"]
A_tot3, Perf_tot3, Perf_area3 = dataPerRun3["A_tot"], dataPerRun3["Perf_tot"], dataPerRun3["Perf_area"]



#crater profile



#table
A_MEAN1 = np.mean(A_tot1)
A_STD1 = np.std(A_tot1)
perf_MEAN1 = np.mean(Perf_tot1)
perf_STD1 = np.std(Perf_tot1)

Crater_area1 = A_tot1-Perf_area1
craterVolumes1 = [(3/8)*Crater_area1[i]*diameters[i]/2 for i in range(len(diameters))]
perfVolumes1 = [Perf_area1[i]*thickness1*10**-3 for i in range(len(diameters))]
CraterEjecta1 = sum(craterVolumes1)
PerfEjecta1 = sum(perfVolumes1)
VER1 = CraterEjecta1 + PerfEjecta1

A_MEAN2 = np.mean(A_tot2)
A_STD2 = np.std(A_tot2)
perf_MEAN2 = np.mean(Perf_tot2)
perf_STD2 = np.std(Perf_tot2)

Crater_area2 = A_tot2-Perf_area2
craterVolumes2 = [(3/8)*Crater_area2[i]*diameters[i]/2 for i in range(len(diameters))]
perfVolumes2 = [Perf_area2[i]*thickness2*10**-3 for i in range(len(diameters))]
CraterEjecta2 = sum(craterVolumes2)
PerfEjecta2 = sum(perfVolumes2)
VER2 = CraterEjecta2 + PerfEjecta2

A_MEAN3 = np.mean(A_tot3)
A_STD3 = np.std(A_tot3)
perf_MEAN3 = np.mean(Perf_tot3)
perf_STD3 = np.std(Perf_tot3)

Crater_area3 = A_tot3-Perf_area3
craterVolumes3 = [(3/8)*Crater_area3[i]*diameters[i]/2 for i in range(len(diameters))]
perfVolumes3 = [Perf_area3[i]*thickness3*10**-3 for i in range(len(diameters))]
CraterEjecta3 = sum(craterVolumes3)
PerfEjecta3 = sum(perfVolumes3)
VER3 = CraterEjecta3 + PerfEjecta3

print(r'Total damage = ${} \pm {}$'.format(A_MEAN1, A_STD1))
print(r'Perforations = ${} \pm {}$'.format(perf_MEAN1, perf_STD1))
print(r'Perforation Area = ${} \pm {}$'.format(np.mean(Perf_area1), np.std(Perf_area1)))
print(r'Crater Area = ${} \pm {}$'.format(Crater_area1,0))
print(r'Crater VER = ${} \pm {}$'.format(CraterEjecta1,0))
print(r'Perforation VER = ${} \pm {}$'.format(PerfEjecta1,0))
print(r'Total VER = ${} \pm {}$'.format(VER1,0))

print(r'Crater VER = ${} \pm {}$'.format(CraterEjecta2,0))
print(r'Perforation VER = ${} \pm {}$'.format(PerfEjecta2,0))
print(r'Total VER = ${} \pm {}$'.format(VER2,0))

print(r'Crater VER = ${} \pm {}$'.format(CraterEjecta3,0))
print(r'Perforation VER = ${} \pm {}$'.format(PerfEjecta3,0))
print(r'Total VER = ${} \pm {}$'.format(VER3,0))


Materials = [materialType,materialType,materialType]
Thickness = [thickness1,thickness2,thickness3]
Perforations = [str(round(perf_MEAN1,1))+'(pm '+str(round(perf_STD1,1))+')',str(round(perf_MEAN2,1))+'(pm '+str(round(perf_STD2,1))+')',str(round(perf_MEAN3,1))+'(pm '+str(round(perf_STD3,1))+')']
PerfFADR = [str(round(np.mean(Perf_area1),8))+'(pm '+str(round(np.std(Perf_area1),8))+')',str(round(np.mean(Perf_area2),8))+'(pm '+str(round(np.std(Perf_area2),8))+')',str(round(np.mean(Perf_area3),8))+'(pm '+str(round(np.std(Perf_area3),8))+')']
TotFADR = [str(round(A_MEAN1,8))+'(pm '+str(round(A_STD1,8))+')',str(round(A_MEAN2,8))+'(pm '+str(round(A_STD2,8))+')',str(round(A_MEAN3,8))+'(pm '+str(round(A_STD3,8))+')']


df = pd.DataFrame(dict(Materials=Materials,Thickness=Thickness, Perforations=Perforations, Perforation_FADR = PerfFADR, Total_FADR = TotFADR))
#print(df.to_latex(index=False))


# Define plotting choices
plotColor = 'steelblue'

errorColor = 'darkslategrey'
errorThickness = 0.5
errorCapsize = 0.5
size = 25
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.style.use("default")
plt.rc('xtick',labelsize=size)
plt.rc('ytick',labelsize=size)
# Plot flux

# AA_MEAN
def Plot_AA_MEAN():
    figAA_MEAN, ax = plt.subplots()

    ax.scatter(np.log10(masses), AA_MEAN1, s=20, color='steelblue', marker="v", label='{}, Thickness = {} mm'.format('ALUMINIUM', 1.0))
    ax.plot(np.log10(masses), AA_MEAN1, color='steelblue',alpha=0.4)
    #ax.errorbar(np.log10(masses), AA_MEAN1, yerr = AA_STD1, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(np.log10(masses), AA_MEAN2, s=20, color="r",marker='x', label='{}, Thickness = {} mm'.format('TITANIUM', 1.0))
    ax.plot(np.log10(masses), AA_MEAN2, color='r',alpha=0.4)
    #ax.errorbar(np.log10(masses), AA_MEAN2, yerr = AA_STD2, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(np.log10(masses), AA_MEAN3, s=20, color="y", label='{}, Thickness = {} mm'.format('CARBONFIBER', 1.0))
    ax.plot(np.log10(masses), AA_MEAN3, color='y',alpha=0.4)
    ax.errorbar(np.log10(masses), AA_MEAN3, yerr = AA_STD3, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
    plt.ylim(0,8*10**-7)
    ax.set_xlabel('$\log$ Masses (kg)', size=size)
    ax.set_ylabel('Damaged area fraction', size=size)
    #ax.set_xscale('log')
    ax.grid()
    ax.legend(fontsize= size)

# CRAT_MEAN
def Plot_CRAT_MEAN():
    figCRAT_MEAN, ax = plt.subplots()

    ax.scatter(masses, np.log10(CRAT_MEAN1), s=20, color='steelblue', marker="v", label='{}, Thickness = {} mm'.format('ALUMINIUM', 1.0))
    ax.plot(masses, np.log10(CRAT_MEAN1), color='steelblue',alpha=0.4)
    ax.errorbar(masses, np.log10(CRAT_MEAN1), yerr = CRAT_STD1, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(masses, np.log10(CRAT_MEAN2), s=20, color='r', marker="x", label='{}, Thickness = {} mm'.format('TITANIUM', 1.0))
    ax.plot(masses, np.log10(CRAT_MEAN2), color='r',alpha=0.4)
    ax.errorbar(masses, np.log10(CRAT_MEAN2), yerr = CRAT_STD2, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")

    ax.scatter(masses, np.log10(CRAT_MEAN3), s=20, color='y', label='{}, Thickness = {} mm'.format('CARBONFIBER', 1.0))
    ax.plot(masses, np.log10(CRAT_MEAN3), color='y',alpha=0.4)
    ax.errorbar(masses, np.log10(CRAT_MEAN3), yerr = CRAT_STD3, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")


    ax.set_xlabel('Masses (kg)', size= size)
    ax.set_ylabel('(log) Craterdepth (m)', size= size)
    ax.set_xscale('log')
    ax.grid()
    ax.legend(fontsize= size)

# Craterdepth profile
def Plot_CRAT_PROFILE():
    figCRAT_PROFILE, ax = plt.subplots()
    ax.scatter(Depths, CRAT_PROFILE, s=5, color=plotColor, label='{}, Thickness = {} mm'.format(materialType.lower(), 0.3))
    #ax.errorbar(np.log10(masses), CRAT_MEAN, yerr = CRAT_STD, ecolor=errorColor, elinewidth=errorThickness, capsize=errorCapsize, fmt='none', marker="none")
    ax.set_xlabel('Craterdepth (m)', size= 15)
    ax.set_ylabel('Cumulative damaged area fraction', size= 15)
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.grid()
    ax.legend(fontsize= 10)

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