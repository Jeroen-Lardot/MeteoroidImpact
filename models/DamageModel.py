import numpy as np

class DamageModel:

    # integral A(m) f(m) dm, where A(m) is given by __areaDamagePerMass
    def areaDamageRate(self, component, environment):
        # Particles which do not penetrate the material and leave a crater:
        A1 = [np.pi*self.diameterHole(component.getThickness(), component.getMaterial(), environment.getVelocities()[i], environment.getDiameters()[i]/100, environment.getDensities()[i])**2 for i in range(len(environment.getMasses()))] # the area a particle of mass m would damage
        perforationIntegral = 0
        for i in range(len(environment.getMasses())-1):
            perforationIntegral =+ A1[i]*environment.getFluxes()[i]* (environment.getMasses()[i+1]-environment.getMasses()[i])

        # Particles which do penetrate the material and leave a hole:

        return perforationIntegral

    # Gives the damaged surface area by a particle of mass m and velocity V, given surface properties
    def areaDamagePerMass(self, mass, particleVelocity, surfaceDensity, surfaceDiameter):
        # TODO
        return None

    # Returns the marginal diameter (micrometer) of the impacting particle at which point the
    # surface diameter (micrometer) will be completely penetrated by a particle of density (g/cm3) and velocity (km/s)
    def __criticalDiameter(self, surfaceDiameter, particleDensity, particleVelocity):
        return (surfaceDiameter / (0.65*particleDensity ** (0.52) * particleVelocity ** (0.875)))**(1/1.056)

    #returns the diameter of the hole created by penetrating particles
    def diameterHole(self, thickness, material, velocity, diameter, density):
        return 3.309 * diameter * (velocity/1)**0.033 * (velocity/material.getSpeedOfSound())**0.298 * (density/material.getDensity())**0.022 * (thickness/diameter)**0.033

    def diameterConchoidal(self, material, density, diameter, velocity):
        return 5*10**(-4) * material.getDensity**(-0.5) * density**0.784 * diameter**1.076 * velocity**0.727

    def diameterCrater(self, material, density, diameter, velocity):
        return 1.12 * 10 ** (-4) * material.getDensity ** (-0.5) * density ** 0.743 * diameter ** 1.076 * velocity ** 0.727
