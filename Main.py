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
N = 10 ** 3
environment = Environment("models/spenvisdata.csv")
spacecraft = Spacecraft(MATERIAL.ALUMINIUM, 0.0003, environment)


def f(input):
    if input % np.ceil(N / 10) == 0:
        print('progress: {}%'.format(input / N * 100))
    return spacecraft.getDamage()


if __name__ == '__main__':

    # Calculate data using multiprocessing to speed up the process
    # with a factor = #number of cpus on the device.
    pool = Pool(multiprocessing.cpu_count())
    results = list(zip(*pool.map(f, [i for i in range(N)])))
    pool.close()
    pool.join()


    # Define data
    A_tot = results[2]
    Perf_tot = results[0]
    Perf_area = [np.sum(item) for item in results[1]]
    Perf_max = [np.max(item) for item in results[1]]
    AA_tot = [[] for i in range(140)]
    Crat_tot = [[] for i in range(140)]
    for i in range(N):
        for j in range(len(AA_tot)):
            AA_tot[j].append(results[3][i][j])
            Crat_tot[j].append(results[4][i][j])


    # Process data
    AA_MEAN = [np.mean(AAtot_bin) for AAtot_bin in AA_tot]
    AA_STD = [np.std(AAtot_bin) for AAtot_bin in AA_tot]
    CRAT_MEAN = [np.mean(CratTot_bin) for CratTot_bin in Crat_tot]
    CRAT_STD = [np.std(CratTot_bin) for CratTot_bin in Crat_tot]
    print(AA_tot[90])
    print(len(AA_tot[90]))
    print(AA_MEAN[90])
    print(AA_STD[90])


    # Save everything to a file
    basename = 'run_{}_{}_{}'.format(N, spacecraft.getMaterial().name, spacecraft.getThickness() * 10 ** 3)
    pathDir = '../Simulation_data/' + basename
    if not os.path.exists('../Simulation_data/'): os.mkdir('../Simulation_data/')
    if not os.path.exists(pathDir): os.mkdir(pathDir)

    dataPerRun = pd.DataFrame({'A_tot': A_tot, 'Perf_tot': Perf_tot, 'Perf_area': Perf_area, 'Perf_max': Perf_max})
    dataPerBin = pd.DataFrame({'AA_MEAN': AA_MEAN, 'AA_STD': AA_STD, 'CRAT_MEAN': CRAT_MEAN, 'CRAT_STD': CRAT_STD})
    dataPerRun.to_csv(pathDir + '/' + 'dataPerRun.csv', sep='\t')
    dataPerBin.to_csv(pathDir + '/' + 'dataPerBin.csv', sep='\t')