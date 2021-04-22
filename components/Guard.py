from components.Component import Component
import numpy as np

class Guard(Component):
    def __init__(self, material, radius, thickness, height):
        super().__init__("Guard", material, radius, thickness)
        self.height = height

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def exposedArea(self):
        return 2*np.pi*self.getRadius()*self.getHeight()
