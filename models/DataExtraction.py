import pandas as pd
from scipy.integrate import trapz
import numpy as np

class DataExtraction:
    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(path, names=["mass", "diameter", "density", "flux"], header=0)
        self.individualFlux = self.__getIndividualFlux()

    def getMasses(self):
        return list(self.df["mass"])

    def getDiameters(self):
        return list(self.df["diameter"])

    def getDensities(self):
        return list(self.df["density"])

    def getFluxes(self):
        return list(self.df["flux"])

    def getIndividualFluxes(self):
        return self.individualFlux

    # Method calculates the individual flux for every mass, instead of the cummulative flux
    def __getIndividualFlux(self):
        indFlux = []
        i = 0    
        indFlux = -np.diff(self.getFluxes())
        np.append(indFlux, self.getFluxes()[len(self.getFluxes())-1])
        
        return indFlux

    # Method calculates the total amount of impacts for a certain area (m^2) and time span (yr), for a certain mass range
    def getImpacts(self, smallest, largest, area, time):
        return (self.getFluxes()[smallest]-self.getFluxes()[largest])*area*time