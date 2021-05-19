from collections import Counter
from random import choices

from Environment import Environment
from Spacecraft import Spacecraft
from models.MATERIAL import MATERIAL
from models.VELOCITY import VELOCITY
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Define a new spacecraft in a new environment
environment = Environment("models/spenvisdata.csv", VELOCITY.TAYLOR)
spacecraft = Spacecraft(environment)

# Add components to spacecraft.
spacecraft.addProbe(MATERIAL.ALUMINIUM, 0.040, 0.003)
spacecraft.addProbe(MATERIAL.ALUMINIUM, 0.040, 0.003)
spacecraft.addGuard(MATERIAL.CARBONFIBER, 0.016, 0.003, 0.1)
spacecraft.addGuard(MATERIAL.CARBONFIBER, 0.016, 0.003, 0.1)
spacecraft.addConalBoom(MATERIAL.CARBONFIBER, 0.01095, 0.050, 0.003, 0.9)
spacecraft.addStraightBoom(MATERIAL.CARBONFIBER, 0.01095, 0.003, 0.9)

# List spacecraft components and total exposed area
print(spacecraft.getComponentNames())
print(spacecraft.getExposedArea(), "m^2")
print(environment.getVelocities())
print(spacecraft.getAreaDamageRates())



velocities = (np.sort(environment.getVelocities()))
#array = dict(Counter(velocities))

df = pd.read_excel('models/Distribution.xlsx', sheet_name='Sheet1', names=["velocity", "probability"])
distribution = choices(df["velocity"], df["probability"],k=10**6)
arrays = dict(Counter(distribution))
average = sum(distribution)/10**6

plt.plot(arrays.keys(), arrays.values(), "b.", label ="Average: "+str(average)+"km/s")
plt.ylabel("Counts")
plt.xlabel("Velocity (km/s)")
plt.title("Taylor velocity model")
plt.legend()
plt.show()