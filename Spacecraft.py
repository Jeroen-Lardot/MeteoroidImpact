from models.DamageModel import DamageModel


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
        return self.damageModel.alternative(self, self.environment)

    # gives total damage area
    def getTotalDamageRates(self):
        return self.damageModel.areaDamageTotal(self, self.environment)

    # Gives area which is perforated
    def getPerforationDamageRate(self):
        return self.damageModel.areaDamagePerforation(self, self.environment)

    # Gives area by craters
    def getCraterDamageRate(self):
        return self.damageModel.areaDamageCrater(self, self.environment)

    # Gives area by conchoidal
    def getConchoidalDamageRate(self):
        return self.damageModel.areaDamageConchoidal(self, self.environment)

    # Gives damaged area up to a certain depth (in meter)
    def getAreaDamageUpToDepth(self, depth):
        return self.damageModel.areaDamageUpToDepth(self, self.environment, depth)

    # Returns the average amount of perforations per year
    def getExpectedPerforations(self):
        return self.damageModel.expectedPerforations(self, self.environment)