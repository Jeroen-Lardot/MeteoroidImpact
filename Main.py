from DataExtraction import DataExtraction

data = DataExtraction(str("spenvisdata.csv"))
print(data.getImpacts(0, 180, 1, 1))
print(data.getIndividualFluxes())





