class DamageModel:
    def __init__(self, diameters, densities, velocities):
        self.diameters = diameters
        self.densities = densities
        self.velocities = velocities

    def isPenetrated(self, surfaceDiameter, particleDensity, particleVelocity):
        if (surfaceDiameter < self.__criticalDiameter(surfaceDiameter, particleDensity, particleVelocity)):
            return True
        else:
            return False

    # Returns the marginal diameter (micrometer) of the impacting particle at which point the
    # surface diameter (micrometer) will be completely penetrated by a particle of density (g/cm3) and velocity (km/s)
    def __criticalDiameter(self, surfaceDiameter, particleDensity, particleVelocity):
        return (surfaceDiameter / (0.65*particleDensity ** (0.52) * particleVelocity ** (0.875)))**(1/1.056)

    # integral A(m) f(m) dm, where A(m) is given by __areaDamagePerMass
    def __areaDamageRate(self, areas, fluxes):
        # TODO
        return None

    # Gives the damaged surface area by a particle of mass m and velocity V, given surface properties
    def __areaDamagePerMass(self, mass, particleVelocity, surfaceDensity, surfaceDiameter):
        # TODO
        return None

