class VelocityModel:
    def __init__(self, masses):
        self.masses = masses
        self.velocities = self.__calculateVelocities()

    def getVelocities(self):
        return self.velocities

    # Method uses the velocity model to calculate an array of velocities for every mass
    def __calculateVelocities(self):
        particleVelocities = []
        for mass in self.masses:
            particleVelocities.append(self.__velocityModel(mass))
        return particleVelocities

    # Velocity model receives a mass and returns a velocity in km/s
    def __velocityModel(self, mass):
        if(mass > 10**(-9)):
            return 7
        if(10**(-16) < mass <= 10**(-9)):
            return self.__line(10**-16, 20, 10**-9, 7, mass)
        if(mass <= 10**(-16)):
            return 20
        return None

    # Returns the Y value of the function Y = f(X), where f(X) is the straight line through (x1,y1) and (x2,y2)
    def __line(self, x1, y1, x2, y2, X):
        a = (y2 - y1) / (x2 - x1)
        return a * (X - x1) + y1
