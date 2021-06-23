from models.DataExtraction import DataExtraction
import pandas as pd

#This class defines the dust environment from the taylor velocity distribution
#and the grün flux.
class Environment:
    def __init__(self, path):
        self.dataExtraction = DataExtraction(path)
        self.velocities = self.__calculateVelocities()


    def getMasses(self):
        return self.dataExtraction.getMasses()

    def getDiameters(self):
        return self.dataExtraction.getDiameters()

    def getDensities(self):
        return self.dataExtraction.getDensities()

    def getFluxes(self):
        return self.dataExtraction.getIndividualFluxes()

    def getVelocities(self):
        return self.velocities

    # Method uses the velocity model to calculate an array of velocities for every mass
    def __calculateVelocities(self):
        return pd.read_excel('models/Distribution.xlsx', sheet_name='Sheet1', names=["velocity", "probability"])


