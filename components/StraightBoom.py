from Component import Component
import numpy as np

class StraightBoom(Component):
    def __init__(self, density, radius, thickness, height):
        super.__init__(self, "StraightBoom", density, radius, thickness)
        self.height = height

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def exposedArea(self):
        return 2*np.pi*self.getRadius()*self.getHeight()