from DataExtraction import DataExtraction
from VelocityModel import VelocityModel
import matplotlib.pyplot as plt

data = DataExtraction(str("spenvisdata.csv"))
velocityData = VelocityModel(data.getMasses())
print(velocityData.getVelocities())

y = []
i=0
for i in range(len(data.getDiameters())):
    y.append(((data.getMasses()[i] / 100) ** 2) * data.getFluxes()[i])

plt.plot(data.getMasses(), y, "b")
plt.savefig("plots/test.png")


