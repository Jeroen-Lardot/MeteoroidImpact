from components.ConalBoom import ConalBoom
from components.Guard import Guard
from components.Probe import Probe
from components.StraightBoom import StraightBoom
from models.DamageModel import DamageModel


class Spacecraft:
    def __init__(self, environment):
        self.damageModel = DamageModel()
        self.environment = environment
        self.components = []

    def addProbe(self, density, radius, thickness):
        self.components.append(Probe(density, radius, thickness))

    def addGuard(self, density, radius, thickness, height):
        self.components.append(Guard(density, radius, thickness, height))

    def addStraightBoom(self, density, radius, thickness, height):
        self.components.append(StraightBoom(density, radius, thickness, height))

    def addConalBoom(self, density, minradius, maxradius, thickness, height):
        self.components.append(ConalBoom(density, minradius, maxradius, thickness, height))

    def getComponentNames(self):
        return [component.getName() for component in self.components]

    def getComponents(self):
        return self.components

    def getExposedArea(self):
        return sum(component.exposedArea() for component in self.components)

    def getAreaDamageRates(self):
        return [self.damageModel.areaDamageRate(component, self.environment) for component in self.components]
