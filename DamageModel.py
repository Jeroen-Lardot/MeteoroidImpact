class DamageModel:
    def __init__(self, diameters, densities, velocities):
        self.diameters = diameters
        self.densities = densities
        self.velocities = velocities

    def isPenetrated(self, sample, diameter, density, velocity):
        if(sample < self.__criticalRadius(diameter, density, velocity)):
            return True
        else:
            return False

    def __criticalRadius(self, diameter, density, velocity):
        return 0.65 * diameter ** (0.056) * density ** (0.52) * velocity ** (0.875)
