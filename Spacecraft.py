from models.DamageModel import DamageModel

#This class creates a spacecraft which is made of a certain material, thickness
# and environment
class Spacecraft:
    def __init__(self, material, thickness ,environment):
        self.material = material
        self.thickness = thickness
        self.damageModel = DamageModel()
        self.environment = environment
        self.components = []

    def setMaterial(self, material):
        self.material = material

    def getMaterial(self):
        return self.material

    def setThickness(self, thickness):
        self.thickness = thickness

    def getThickness(self):
        return self.thickness

    def getDamage(self):
        return self.damageModel.monte_carlo(self, self.environment)
