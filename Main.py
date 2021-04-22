from Environment import Environment
from Spacecraft import Spacecraft
from models.MATERIAL import MATERIAL
from models.VELOCITY import VELOCITY

#Define a new spacecraft in a new environment
environment = Environment("models/spenvisdata.csv", VELOCITY.LOGARITHMIC)
spacecraft = Spacecraft(environment)

#Add components to spacecraft.
spacecraft.addProbe(MATERIAL.ALUMINIUM, 0.040, 0.003)
spacecraft.addProbe(MATERIAL.ALUMINIUM, 0.040, 0.003)
spacecraft.addGuard(MATERIAL.CARBONFIBER, 0.016, 0.003, 0.1)
spacecraft.addGuard(MATERIAL.CARBONFIBER, 0.016, 0.003, 0.1)
spacecraft.addConalBoom(MATERIAL.CARBONFIBER, 0.01095, 0.050, 0.003, 0.9)
spacecraft.addStraightBoom(MATERIAL.CARBONFIBER, 0.01095, 0.003, 0.9)

#List spacecraft components and total exposed area
print(spacecraft.getComponentNames())
print(spacecraft.getExposedArea(), "m^2")
print(environment.getVelocities())
print(spacecraft.getAreaDamageRates())


