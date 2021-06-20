from Environment import Environment
from Spacecraft import Spacecraft
from models.MATERIAL import MATERIAL
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
from multiprocessing import Pool
import multiprocessing
#Take a multiprocessing approach

# Define a new spacecraft in a new environment
environment = Environment("models/spenvisdata.csv")
spacecraft = Spacecraft(MATERIAL.TITANIUM, 0.0003, environment)




"""
print("Perforation: {}".format(spacecraft.getPerforationDamageRate()))
print("Total: {}".format(spacecraft.getTotalDamageRates()))
print("Crater: {}".format(spacecraft.getCraterDamageRate()))
print("Conchoidal: {}".format(spacecraft.getConchoidalDamageRate()))
depth = 1*10**-6 #in meters
print("Area damaged deeper than {:.3f} micrometers: {}".format(depth*10**6, spacecraft.getAreaDamageUpToDepth(depth))) #depth in meters
print("Average degradation liftetime (yr): {}".format([1/((365*24*3600)*ADR) for ADR in spacecraft.getTotalDamageRates()]))
print("Average amount of perforations per year: {}".format(spacecraft.getExpectedPerforations()))
"""


#Run for every material and its thickness variations

N = 10**3

AA_tot = [ [] for i in range(140)]
Crat_tot = [ [] for i in range(140)]

A_tot = []
Perf_tot =[]
Perf_area = []
Perf_max = []


for i in range(N):
    if i%np.ceil(N/50) ==0:
        print('progress: {}%'.format(i/N*100))
    perforations, perforationsArea, A_total, AA, craterDepth = spacecraft.getDamage()

    A_tot.append(A_total)
    Perf_tot.append(perforations)
    Perf_area.append(np.sum(perforationsArea))
    Perf_max.append(np.max(perforationsArea))
    
    for k in range(len(AA_tot)):
        AA_tot[k].append(AA[k])
        Crat_tot[k].append(craterDepth[k])
    

AA_MEAN = [np.mean(AAtot_bin) for AAtot_bin in AA_tot]
AA_STD = [np.std(AAtot_bin) for AAtot_bin in AA_tot]

CRAT_MEAN = [np.mean(CratTot_bin) for CratTot_bin in Crat_tot]
CRAT_STD = [np.std(CratTot_bin) for CratTot_bin in Crat_tot]



#print([Perf_tot, A_tot, AA_tot, craterDepth])

depth = 1*10**-6 # in m
A_depth = 0

#for i in range(len(CRAT_MEAN)):
#    if craterDepth[i] > depth:
#        A_depth += AA[i]

x=[]
for i in range(len(environment.getMasses())-1):
    x.append(environment.getMasses()[i])

#plt.plot(np.log10(x),AA_tot ,"b-")
#plt.show()

#df = pd.DataFrame(dict(Mass=x,AreaDamage=AA_tot))
#print(df.to_latex(index=False))

print("max perforation area") 
print(Perf_max, Perf_area)

# Save everything to a file
basename = 'run_{}_{}_{}'.format(N, spacecraft.getMaterial(), spacecraft.getThickness()*10**3)
if not os.path.exists('../Simulation_data/'):
    os.mkdir('../Simulation_data/')
    
pathDir = '../Simulation_data/' + basename
if not os.path.exists(pathDir):
    os.mkdir(pathDir)
    
print(len(A_tot), len(AA_MEAN),len(AA_STD), len(Perf_tot), len(CRAT_MEAN), len(CRAT_STD))
print(A_tot,Perf_tot)


dataPerRun = pd.DataFrame({'A_tot': A_tot, 'Perf_tot': Perf_tot, 'Perf_area': Perf_area, 'Perf_max':Perf_max})

dataPerBin = pd.DataFrame({'AA_MEAN': AA_MEAN,
                           'AA_STD': AA_STD,
                           'CRAT_MEAN': CRAT_MEAN,
                           'CRAT_STD': CRAT_STD})

dataPerRun.to_csv(pathDir + '/' + 'dataPerRun.csv',sep='\t')
dataPerBin.to_csv(pathDir + '/' + 'dataPerBin.csv',sep='\t')

"""
df = pd.read_excel('models/Distribution.xlsx', sheet_name='Sheet1', names=["velocity", "probability"])
distribution = choices(df["velocity"], df["probability"],k=10**6)
arrays = dict(Counter(distribution))
average = sum(distribution)/10**6
print(len(environment.getMasses()))
x = np.linspace(1,182,181)
plt.plot(np.log(environment.getMasses()),environment.getVelocities(),'b.')
plt.show()

plt.plot(arrays.keys(), arrays.values(), "b.", label ="Average: "+str(average)+"km/s")
plt.ylabel("Counts")
plt.xlabel("Velocity (km/s)")
plt.title("Taylor velocity model")
plt.legend()
plt.show()
"""