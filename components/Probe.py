from components.Component import Component
import numpy as np

class Probe(Component):
    def __init__(self, material, radius, thickness):
        super().__init__("Probe", material, radius, thickness)

    def exposedArea(self):
        return 4*np.pi*self.getRadius()**2


