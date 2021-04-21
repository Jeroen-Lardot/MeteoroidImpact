from Component import Component
import numpy as np

class ConalBoom(Component):
    def __init__(self, density, minradius, maxradius, thickness, height):
        super.__init__(self, "ConalBoom", density, 0, thickness)
        self.height = height
        self.minradius = minradius
        self.maxradius = maxradius

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def getMinRadius(self):
        return self.minradius

    def setMinRadius(self, minradius):
        self.minradius = minradius

    def getMaxRadius(self):
        return self.maxradius

    def setMaxRadius(self, maxradius):
        self.maxradius = maxradius

    def exposedArea(self):
        return np.pi * (self.getMinRadius() + self.getMaxRadius()) * np.sqrt((self.getMaxRadius-self.getMinRadius)**2+self.getHeight()**2) + np.pi * (self.getMinRadius()**2+self.getMaxRadius()**2)