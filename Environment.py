from models.DataExtraction import DataExtraction
from models.VELOCITY import VELOCITY

class Environment:
    def __init__(self, path, velocityModel):
        self.dataExtraction = DataExtraction(path)
        self.velocityModel = velocityModel
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
        return self.velocityModel.getVelocity(1)

    # Method uses the velocity model to calculate an array of velocities for every mass
    def __calculateVelocities(self):
        particleVelocities = []
        for mass in self.dataExtraction.getMasses():
            particleVelocities.append(self.velocityModel.getVelocity(mass))
        return particleVelocities


