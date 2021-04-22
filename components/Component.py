class Component:
    def __init__(self, name, material, radius, thickness):
        self.name = name
        self.material = material
        self.radius = radius
        self.thickness = thickness

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getMaterial(self):
        return self.material

    def setMaterial(self, material):
        self.material = material

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
