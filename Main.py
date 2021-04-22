from Environment import Environment
from Spacecraft import Spacecraft
from models.VELOCITY import VELOCITY

spacecraft = Spacecraft()
environment = Environment("models/spenvisdata.csv", VELOCITY.LOGARITHMIC)

#Add components to spacecraft.
spacecraft.addProbe(2.7, 0.040, 0.003)
spacecraft.addProbe(2.7, 0.040, 0.003)
spacecraft.addGuard(2.7, 0.016, 0.003, 0.1)
spacecraft.addGuard(2.7, 0.016, 0.003, 0.1)
spacecraft.addConalBoom(2.7, 0.01095, 0.050, 0.003, 0.9)
spacecraft.addStraightBoom(2.7, 0.01095, 0.003, 0.9)

#List spacecraft components
spacecraft.listComponents()
print(spacecraft.getComponents()[4].exposedArea())

