from DataExtraction import DataExtraction
from VelocityModel import VelocityModel

data = DataExtraction(str("spenvisdata.csv"))
velocityData = VelocityModel(data.getMasses())
print(velocityData.getVelocities())






