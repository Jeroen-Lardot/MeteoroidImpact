from models.DataExtraction import DataExtraction
from models.VELOCITY import VELOCITY


class Environment:
    def __init__(self, path, velocityModel):
        self.dataExtraction = DataExtraction(path)
        self.velocityModel = velocityModel
        self.velocities = self.__calculateVelocities()


    # Method uses the velocity model to calculate an array of velocities for every mass
    def __calculateVelocities(self):
        particleVelocities = []
        for mass in self.dataExtraction.getMasses():
            particleVelocities.append(VELOCITY.velocity(self.velocityModel,mass))
        print(particleVelocities)
        return particleVelocities
