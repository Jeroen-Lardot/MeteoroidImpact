import numpy as np
from scipy.integrate import trapz
from scipy.integrate import simps
import random

import matplotlib.pyplot as plt
#from models.DataExtraction import DataExtraction
from models.VELOCITY import VELOCITY
from Environment import Environment
import time
from scipy import stats
import concurrent.futures
import scipy.interpolate as interpolate
from collections import Counter

class DamageModel:
    def __init__(self):
        environment = Environment("models/spenvisdata.csv", VELOCITY.TAYLOR)
        self.velocities = environment.getVelocities()["velocity"]*1000  # gives velocities in km/s
        self.velocityDistribution = environment.getVelocities()["probability"]  # dimensionless probability function

        self.masses = [mass * 0.001 for mass in environment.getMasses()]  # gives masses in kg
        self.IndividualFluxes = [flux for flux in environment.getFluxes()]  # gives flux in 1/(m^2 * yr)
        # Get diameters and densities for the particles
        self.diameters = [diameter * 0.01 for diameter in environment.getDiameters()]  # gives diameters in m
        self.densities = [density * 1000 for density in environment.getDensities()]  # gives densities in kg/m^-3


    def andereBoeg(self, component, environment):
        begin = time.perf_counter()

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
                d_c = self.__criticalDiameter(component.getThickness(), density, velocity)
                if diameter > d_c:
                    #This mean there will be a perforation
                    A_perf = np.pi*(self.diameterHole(component.getThickness(), component.getMaterial(), velocity, diameter, density)/2)**2  # the area a particle of mass m and velocity v would damage
                    A = A + A_perf
                    
                    perforationsArea.append(A_perf)
                    perforations += 1
                    craterDepth = [0]
                else:
                    conchoidal = self.diameterConchoidal(component.getMaterial(), density, diameter, velocity)
                    diameterCrater = self.diameterCrater(component.getMaterial(), density, diameter, velocity)
                    craterDepth.append(diameterCrater/2)
                    A = A + np.pi*(conchoidal/2)**2


            AA.append(A)
            CRATERDEPTH.append(np.mean(craterDepth))

        A_total = np.sum(AA)

        return [perforations, perforationsArea, A_total, AA, CRATERDEPTH]


    def areaDamageTotal(self, component, environment):
        AA, DIAM, masses, velocities = self.areaDamageIntegral(component, environment, "Total")
        totalDamage = trapz([trapz(AA_mass,masses) for AA_mass in AA], velocities)         
        return totalDamage
    
    def areaDamagePerforation(self, component, environment):            
        AA, DIAM, masses, velocities = self.areaDamageIntegral(component, environment, "Hole")
        totalDamage = trapz([trapz(AA_mass,masses) for AA_mass in AA], velocities) 
        return totalDamage
            
    def areaDamageCrater(self, component, environment):
        AA, DIAM, masses, velocities = self.areaDamageIntegral(component, environment, "Crater")
        totalDamage = trapz([trapz(AA_mass,masses) for AA_mass in AA], velocities) 
        return totalDamage
    
    def areaDamageConchoidal(self, component, environment):
        AA, DIAM, masses, velocities = self.areaDamageIntegral(component, environment, "Conchoidal")
        totalDamage = trapz([trapz(AA_mass,masses) for AA_mass in AA], velocities) 
        return totalDamage
    
    def areaDamageUpToDepth(self, component, environment, depth):
        AA, DIAM, masses, velocities = self.areaDamageIntegral(component, environment, "Crater")
        for i in range(len(DIAM)):
            for j in range(len(DIAM[0])):
                # If the crater is smaller than the depth, set its contribution to zero
                # this way we get the area damaged deeper than depth
                if DIAM[i][j]/2 < depth:
                    AA[i][j] = 0

        areadamageUpToDepth = trapz([trapz(AA_mass,masses) for AA_mass in AA], velocities) 
        return areadamageUpToDepth
    
    
    # Simply creates same grid as elsewhere and sets the valu to 1 if there is a perforation and 0 else. 
    # Then multiply with FF to get frequencies and add it all up
    def expectedPerforations(self, component, environment):
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
                if diameter > self.__criticalDiameter(component.getThickness(), densities[i%len(diameters)], velocity):
                   diamBoolean_flat[i] = 1 
                i += 1
                
        diamBoolean = diamBoolean_flat.reshape(array_shape)
        frequencyPerforations = diamBoolean*FF
        return trapz([trapz(freq,masses) for freq in frequencyPerforations], velocities)

    
        
    # Returns the area and other arrays necessary to calculate the integral:
    # damageType: 'Total', 'Holes', 'Crater', 'Conchoidal'
    def areaDamageIntegral(self, component, environment, damageType):        
        
        # Get velocity/ flux distribution
        velocities = environment.getVelocities()["velocity"]*1000 #gives velocities in km/s
        velocityDistribution = environment.getVelocities()["probability"] #dimensionless probability function
        
        masses = [mass*0.001 for mass in environment.getMasses()] #gives masses in gram
        IndividualFluxes = [flux for flux in environment.getFluxes()] #gives flux in 1/(m^2 * yr)
        
        # Get diameters and densities for the particles
        
        diameters = [diameter*0.01 for diameter in environment.getDiameters()] # gives diameters in cm
        densities = [density*1000 for density in environment.getDensities()] # gives densities in g/cm^-3

        # Make a meshgrid with the frequency of masses in MF and of velocities in VF
        MF, VF = np.meshgrid(IndividualFluxes, velocityDistribution)
        
        # We multiply every element of MF with VF to get an array with all the frequencies
        # which correspond to a certain mass and velocity
        FF = np.multiply(MF, VF)
        array_shape = np.shape(FF)
        
        AA_flat = np.zeros(len(IndividualFluxes)*len(velocityDistribution))
        DIAM_flat = np.zeros(len(IndividualFluxes)*len(velocityDistribution))
        
        i=0
        for velocity in velocities:
            for mass in masses:
                if damageType=="Crater":
                    DIAM_flat[i] = self.AreaDamage(component, mass, velocity, diameters[i%len(masses)], densities[i%len(masses)], damageType)[1]
                    AA_flat[i] = self.AreaDamage(component, mass, velocity, diameters[i%len(masses)], densities[i%len(masses)], damageType)[0]
                else:
                    AA_flat[i] = self.AreaDamage(component, mass, velocity, diameters[i%len(masses)], densities[i%len(masses)], damageType)
                i+=1
                
        # Create an array AA with the area damage corresponding to that 
        # value of mass and velocity and this is weighted with the frequencies FF
        AA = np.multiply(AA_flat.reshape(array_shape),FF)
        DIAM = np.multiply(DIAM_flat.reshape(array_shape),FF)   
        
        print(trapz([trapz(f,masses) for f in FF], velocities))      

        return [AA, DIAM, masses, velocities]
      
    
    
    # Gives the damages surface for a specific particle velocity (km/s) and mass (gram)
    # Damagetype can be: 'Total', 'Holes', 'Crater', 'Conchoidal'
    # For 'Crater' an addition parameter 'CraterDepth' can be added to give the area damaged up to a certain depth (Default 'max': all depths)
    def AreaDamage(self, component, mass, particleVelocity, diameter, density, damageType):
        # critical diamater determining wether a  hole is formed or not
        diameter_crit = self.__criticalDiameter(component.getThickness(), density, particleVelocity)
        if damageType=="Total":
            if (diameter >= diameter_crit):
                #print("hit")
                A_hole = np.pi*(self.diameterHole(component.getThickness(), component.getMaterial(), particleVelocity, diameter, density)/2)**2  # the area a particle of mass m and velocity v would damage
                return A_hole
            else:
                A_conchoidal = np.pi*(self.diameterConchoidal(component.getMaterial(), density, diameter, particleVelocity)/2)**2
                return A_conchoidal
        
        elif damageType=="Hole":
            if (diameter >= diameter_crit):
                A_hole = np.pi*(self.diameterHole(component.getThickness(), component.getMaterial(), particleVelocity, diameter, density)/2)**2  # the area a particle of mass m and velocity v would damage      
                return A_hole
            else:
                return 0
        
        elif damageType=="Crater":
            # Dont count damage where there is perforation
            if diameter >= diameter_crit:
                return [0,self.diameterHole(component.getThickness(), component.getMaterial(), particleVelocity, diameter, density)]
            else:
                diameter_crater = self.diameterCrater(component.getMaterial(), density, diameter, particleVelocity)
                A_crater = np.pi*(diameter_crater/2)**2
                return [A_crater, diameter_crater]
            
        elif damageType=="Conchoidal":
            # Dont count damage where there is perforation
            if (diameter >= diameter_crit):
               return 0
            else:
                A_conchoidal = (np.pi*self.diameterConchoidal(component.getMaterial(), density, diameter, particleVelocity)/2)**2
                return A_conchoidal
        else:
            print("ERROR: Damagetype must be: 'Total', 'Hole', 'Crater' or 'Conchoidal'")
            return


    # Gives the damaged surface area by a particle of mass m and velocity V, given surface properties
    def areaDamagePerMass(self, mass, particleVelocity, surfaceDensity, surfaceDiameter):
        # TODO
        return None

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