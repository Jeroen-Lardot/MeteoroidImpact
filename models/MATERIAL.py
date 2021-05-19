from enum import Enum, auto

class MATERIAL(Enum):
    ALUMINIUM = "Al"
    CARBONFIBER = "CF"
    IRON = "Fe"

    #returns material density in g/cm^3
    def getDensity(self):
        if self == MATERIAL.ALUMINIUM:
            return 2.7
        if self == MATERIAL.CARBONFIBER:
            return 2

    #returns speed of sound in km/s
    def getSpeedOfSound(self):
        if self == MATERIAL.ALUMINIUM:
            return 6.420
        if self == MATERIAL.CARBONFIBER:
            return 10.763
