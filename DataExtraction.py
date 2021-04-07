import pandas as pd

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

    def __getIndividualFlux(self):
        indFlux = []
        i = 0
        for i in range(len(self.getFluxes())-1):
            indFlux.append(self.getFluxes()[i]-self.getFluxes()[i+1])
        indFlux.append(self.getFluxes()[len(self.getFluxes())-1])
        return indFlux

    def getImpacts(self, smallest, largest, area, time):
        return (self.getFluxes()[smallest]-self.getFluxes()[largest])*area*time