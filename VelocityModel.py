class VelocityModel:
    def __init__(self, masses):
        self.masses = masses
        self.velocities = self.__calculateVelocities()

    def getVelocities(self):
        return self.velocities

    def __calculateVelocities(self):
        particleVelocities = []
        for mass in self.masses:
            particleVelocities.append(self.__velocityModel(mass))
        return particleVelocities

    def __velocityModel(self, mass):
        if(mass > 2):
            return 1
        if(1 < mass <= 2):
            return 0
        if(mass <= 1):
            return -1
        return None