class Component:
    def __init__(self, name, density, radius, thickness):
        self.name = name
        self.density = density
        self.radius = radius
        self.thickness = thickness

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getDensity(self):
        return self.density

    def setDensity(self, density):
        self.density = density

    def getRadius(self):
        return self.radius

    def setRadius(self, radius):
        self.radius = radius

    def getThickness(self):
        return self.thickness

    def setThickness(self, thickness):
        self.thickness = thickness

    def exposedArea(self):
        return 0
