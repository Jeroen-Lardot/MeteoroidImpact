class VelocityModel:
    def __init__(self, data):
        self.data = data

    def setVelocityModel(self):
        return list(self.df["mass"])