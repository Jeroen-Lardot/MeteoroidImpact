from Environment import Environment
from Spacecraft import Spacecraft
from models.MATERIAL import MATERIAL
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
from multiprocessing import Pool
import multiprocessing
from numba import jit,cuda

# Specify variables for the run
N = 10000
environment = Environment("models/spenvisdata.csv")
spacecraft = Spacecraft(MATERIAL.ALUMINIUM, 0.0010, environment)


def f(input):
    if input % np.ceil(N / 10) == 0:
        print('progress: {}%'.format(input / N * 100))
    return spacecraft.getDamage()


if __name__ == '__main__':

    # Calculate data using multiprocessing to speed up the process
    # with a factor = #number of cpus on the device.
    pool = Pool(multiprocessing.cpu_count()-1)
    results = list(zip(*pool.map(f, [i for i in range(N)])))
    pool.close()
    pool.join()
    print('progress: {}%'.format(100.0))
    print('Processing Data...')

    # Define data
    A_tot = results[2]
    Perf_tot = results[0]
    binSubTotals = results[5]
    craterSubTotals = results[4]

    Perf_area = []
    Perf_max = []
    for item in results[1]:
        Perf_area.append(np.sum(item))
        if len(item) == 0:
            Perf_max.append(0)
        else:
            Perf_max.append(np.max(item))


    binTotals = [[] for i in range(112)]
    craterTotals = [[] for i in range(112)]
    for i in range(len(binTotals)):
        for j in range(len(binSubTotals)):
            binTotals[i].extend(binSubTotals[j][i])
            craterTotals[i].extend(craterSubTotals[j][i])


    N2 = 0 # The total amount of particles we studied
    for i in range(len(binTotals)):
        N2 = N2 + len(binTotals[i])

    print("Calculating Bins...")
    binMEAN = [[] for i in range(112)]
    binSTD = [[] for i in range(112)]
    craterMEAN = [[] for i in range(112)]
    craterSTD = [[] for i in range(112)]
    for i in range(len(binTotals)):
        binMEAN[i] = (len(binTotals[i])/N2) * np.average(binTotals[i])*8.00*10**3 #times flux to get yearly particle damage
        binSTD[i] = (len(binTotals[i])/N2) * np.std(binTotals[i])*8.00*10**3
        craterMEAN[i] = np.average(binTotals[i])
        craterSTD[i] = np.std(binTotals[i])

    binMEAN = pd.DataFrame(binMEAN).fillna(0)
    binSTD = pd.DataFrame(binSTD).fillna(0)
    craterMEAN = pd.DataFrame(craterMEAN).fillna(0)
    craterSTD = pd.DataFrame(craterSTD).fillna(0)
    #print(binMEAN)
    bin_MEAN = binMEAN[0].tolist()
    bin_STD = binSTD[0].tolist()
    crater_MEAN = craterMEAN[0].tolist()
    crater_STD = craterSTD[0].tolist()
    # Process data
    AA_MEAN = bin_MEAN
    AA_STD = bin_STD

    print("Saving File...")
    # Save everything to a file
    basename = 'run_{}_{}_{}'.format(N, spacecraft.getMaterial().name, spacecraft.getThickness() * 10 ** 3)
    pathDir = '../Simulation_data/' + basename
    if not os.path.exists('../Simulation_data/'): os.mkdir('../Simulation_data/')
    if not os.path.exists(pathDir): os.mkdir(pathDir)

    dataPerRun = pd.DataFrame({'A_tot': A_tot, 'Perf_tot': Perf_tot, 'Perf_area': Perf_area, 'Perf_max': Perf_max})
    dataPerBin = pd.DataFrame({'AA_MEAN': AA_MEAN, 'AA_STD': AA_STD, 'CRAT_MEAN': crater_MEAN, 'CRAT_STD': crater_STD})
    dataPerRun.to_csv(pathDir + '/' + 'dataPerRun.csv', sep='\t')
    dataPerBin.to_csv(pathDir + '/' + 'dataPerBin.csv', sep='\t')
    print("File Saved!")