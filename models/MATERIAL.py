from enum import Enum, auto

#Defines the properties of materials to be studied.
class MATERIAL(Enum):
    ALUMINIUM = "Al"
    CARBONFIBER = "CF"
    TITANIUM = "Ti"


    #returns material density in kg/m^3
    def getDensity(self):
        if self == MATERIAL.ALUMINIUM:
            return 2700
        if self == MATERIAL.CARBONFIBER:
            return 1550
        if self == MATERIAL.TITANIUM:
            return 4506

    #returns speed of sound in m/s
    def getSpeedOfSound(self):
        if self == MATERIAL.ALUMINIUM:
            return 6420
        if self == MATERIAL.CARBONFIBER:
            return 3000
        if self == MATERIAL.TITANIUM:
            return 5090
