import numpy as np
from scipy.integrate import trapz
from scipy.integrate import simps
import random

import matplotlib.pyplot as plt
#from models.DataExtraction import DataExtraction
from Environment import Environment
import time
from scipy import stats
import concurrent.futures
import scipy.interpolate as interpolate
from collections import Counter

class DamageModel:
    def __init__(self):
        environment = Environment("models/spenvisdata.csv")
        self.velocities = environment.getVelocities()["velocity"]*1000  # gives velocities in m/s

        self.velocityDistribution = environment.getVelocities()["probability"]  # dimensionless probability function

        self.masses = [mass * 0.001 for mass in environment.getMasses()]  # gives masses in kg
        self.IndividualFluxes = [flux for flux in environment.getFluxes()]  # gives flux in 1/(m^2 * yr)
        # Get diameters and densities for the particles
        self.diameters = [diameter * 0.01 for diameter in environment.getDiameters()]  # gives diameters in m
        self.densities = [density * 1000 for density in environment.getDensities()]  # gives densities in kg/m^-3



    def createDictionaries(self, spacecraft):
        criticalDiameterDictionary = dict()
        for velocity in self.velocities:
            criticalDiameterDictionary[velocity] = self.__criticalDiameter(spacecraft.getThickness(), 2000.0, velocity)

    def alternative(self, spacecraft, environment):
        AA = []
        CRATERDEPTH = [[] for i in range(112)]
        binCounter = [[] for i in range(112)]
        looptime = []
        counts = []
        perforations = 0
        perforationsArea = []
        i=0
        for f_count in range(len(self.IndividualFluxes)):
            N = np.int(self.IndividualFluxes[f_count])  # amount of particles in this bin
            diameter = self.diameters[f_count]
            density = self.densities[f_count]
            if N >= 1:
                randomVelocities = np.random.choice(self.velocities, N,
                                                    p=self.velocityDistribution / np.sum(self.velocityDistribution))
            else:
                a = random.uniform(0, 1)
                if a <= self.IndividualFluxes[f_count]:
                    N = 1
                else:
                    N = 0
                randomVelocities = np.random.choice(self.velocities, N,
                                                    p=self.velocityDistribution / np.sum(self.velocityDistribution))

            ### Create a pool of processes. By default, one is created for each CPU in your machine.
            A = 0

            for velocity in randomVelocities:

                begin = time.perf_counter()
                d_c = self.__criticalDiameter(spacecraft.getThickness(), density, velocity)
                #print("Time taken: ", time.perf_counter() - begin)
                if diameter > d_c:
                    # This mean there will be a perforation
                    A_perf = np.pi * (self.diameterHole(spacecraft.getThickness(), spacecraft.getMaterial(), velocity,
                                                        diameter,
                                                        density) / 2) ** 2  # the area a particle of mass m and velocity v would damage
                    A = A + A_perf

                    #perforationsArea.append(A_perf)
                    perforations += 1
                    #CRATERDEPTH[i].append(spacecraft.getThickness())
                    #binCounter[i].append(A_perf)
                else:
                    conchoidal = self.diameterConchoidal(spacecraft.getMaterial(), density, diameter, velocity)
                    diameterCrater = self.diameterCrater(spacecraft.getMaterial(), density, diameter, velocity)
                    #CRATERDEPTH.append(diameterCrater / 2)
                    A_conch = np.pi * (conchoidal / 2) ** 2
                    #A = A + A_conch
                    binCounter[i].append(A_conch)
            AA.append(A)
            i=i+1
        A_total = np.sum(AA)
        return [perforations, perforationsArea, A_total, AA, CRATERDEPTH, binCounter]


    def andereBoeg(self, spacecraft, environment):

        AA = []
        CRATERDEPTH = []

        looptime = []
        counts = []
        perforations = 0
        perforationsArea = []
        for f_count in range(len(self.IndividualFluxes)):
            N = np.int(self.IndividualFluxes[f_count]) #amount of particles in this bin
            diameter = self.diameters[f_count]
            density = self.densities[f_count]

            if N >= 1:
                randomVelocities = np.random.choice(self.velocities, N,
                                                    p=self.velocityDistribution / np.sum(self.velocityDistribution))
                craterDepth = []
            else:
                a = random.uniform(0, 1)
                if a <= self.IndividualFluxes[f_count]:
                    N_random = 1
                    craterDepth = []
                else:
                    N_random = 0
                    craterDepth = [0]
                randomVelocities = np.random.choice(self.velocities, N_random,
                                                    p=self.velocityDistribution / np.sum(self.velocityDistribution))

            ### Create a pool of processes. By default, one is created for each CPU in your machine.
            A=0

            for velocity in randomVelocities:
                begin = time.perf_counter()
                d_c = self.__criticalDiameter(spacecraft.getThickness(), density, velocity)
                print("Time taken: ", time.perf_counter() - begin)
                if diameter > d_c:
                    #This mean there will be a perforation
                    A_perf = np.pi * (self.diameterHole(spacecraft.getThickness(), spacecraft.getMaterial(), velocity, diameter, density) / 2) ** 2  # the area a particle of mass m and velocity v would damage
                    A = A + A_perf

                    perforationsArea.append(A_perf)
                    perforations += 1
                    craterDepth = [0]
                else:
                    conchoidal = self.diameterConchoidal(spacecraft.getMaterial(), density, diameter, velocity)
                    diameterCrater = self.diameterCrater(spacecraft.getMaterial(), density, diameter, velocity)
                    craterDepth.append(diameterCrater/2)
                    A = A + np.pi*(conchoidal/2)**2

            AA.append(A)
            CRATERDEPTH.append(np.mean(craterDepth))

        A_total = np.sum(AA)
        return [perforations, perforationsArea, A_total, AA, CRATERDEPTH]




    # Simply creates same grid as elsewhere and sets the valu to 1 if there is a perforation and 0 else.
    # Then multiply with FF to get frequencies and add it all up
    def expectedPerforations(self, spacecraft, environment):
        # Get velocity/ flux distribution
        velocities = environment.getVelocities()["velocity"]*1000 #gives velocities in km/s
        velocityDistribution = environment.getVelocities()["probability"] #dimensionless probability function

        masses = [mass*0.001 for mass in environment.getMasses()] #gives masses in gram
        IndividualFluxes = [flux     for flux in environment.getFluxes()] #gives flux in 1/(m^2 * yr)

        # Get diameters and densities for the particles

        diameters = [diameter*0.01 for diameter in environment.getDiameters()] # gives diameters in cm
        densities = [density*1000 for density in environment.getDensities()] # gives densities in g/cm^-3

        # Make a meshgrid with the frequency of masses in MF and of velocities in VF
        MF, VF = np.meshgrid(IndividualFluxes, velocityDistribution)

        # We multiply every element of MF with VF to get an array with all the frequencies
        # which correspond to a certain mass and velocity
        FF = np.multiply(MF, VF)
        array_shape = np.shape(FF)

        # An array which will be one when the diameter is larger than d_crit and 0 if it is smaller
        diamBoolean_flat = np.zeros(len(IndividualFluxes)*len(velocityDistribution))

        i=0
        for velocity in velocities:
            for diameter in diameters:
                if diameter > self.__criticalDiameter(spacecraft.getThickness(), densities[i%len(diameters)], velocity):
                   diamBoolean_flat[i] = 1
                i += 1

        diamBoolean = diamBoolean_flat.reshape(array_shape)
        frequencyPerforations = diamBoolean*FF
        return trapz([trapz(freq,masses) for freq in frequencyPerforations], velocities)


    # Returns the marginal diameter (micrometer) of the impacting particle at which point the
    # surface diameter (micrometer) will be completely penetrated by a particle of density (g/cm3) and velocity (km/s)
    # Local conversion from SI to CGS and returns back a SI unit
    def __criticalDiameter(self, surfaceDiameter, particleDensity, particleVelocity):
        return 10**-6*(surfaceDiameter*10**6 / (0.65*(particleDensity/1000) ** (0.52) * (particleVelocity/1000) ** (0.875)))**(1/1.056)

    #returns the diameter of the hole created by penetrating particles
    def diameterHole(self, thickness, material, velocity, diameter, density):
        return 3.309 * diameter * (velocity/4000)**0.033 * (velocity/material.getSpeedOfSound())**0.298 * (density/material.getDensity())**0.022 * (thickness/diameter)**0.359
        
    #Local conversion from SI to CGS and returns back a SI unit
    def diameterConchoidal(self, material, density, diameter, velocity):
        return (5*10**(-4) * (material.getDensity()/1000)**(-0.5) * (density/1000)**0.784 * (diameter*100)**1.076 * (velocity*100)**0.727)/100

    # Local conversion from SI to CGS and returns back a SI unit
    def diameterCrater(self, material, density, diameter, velocity):
        return (1.12 * 10 ** (-4) * (material.getDensity()/1000) ** (-0.5) * (density/1000) ** 0.743 * (diameter*100) ** 1.076 * (velocity*100) ** 0.727)/100