class VelocityModel:
    def __init__(self, data):
        self.data = data

    def setDamageModel(self):
        return list(self.df["mass"])