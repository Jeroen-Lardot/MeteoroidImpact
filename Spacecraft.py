from components.ConalBoom import ConalBoom
from components.Guard import Guard
from components.Probe import Probe
from components.StraightBoom import StraightBoom


class Spacecraft:
    def __init__(self):
        self.components = []

    def addProbe(self, density, radius, thickness):
        self.components.append(Probe(density, radius, thickness))

    def addGuard(self, density, radius, thickness, height):
        self.components.append(Guard(density, radius, thickness, height))

    def addStraightBoom(self, density, radius, thickness, height):
        self.components.append(StraightBoom(density, radius, thickness, height))

    def addConalBoom(self, density, minradius, maxradius, thickness, height):
        self.components.append(ConalBoom(density, minradius, maxradius, thickness, height))

    def listComponents(self):
        print([self.components[component].getName() for component in self.components])

    def getComponents(self):
        return self.components

