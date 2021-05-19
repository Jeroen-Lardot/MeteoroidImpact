from enum import Enum, auto
import numpy as np
from random import choices
import pandas as pd

class VELOCITY(Enum):

    LOGARITHMIC = auto()
    LINEAR = auto()
    TAYLOR = auto()
    RANDOM = auto()

    def getVelocity(self, mass):
        if (self == VELOCITY.LOGARITHMIC):
            return self.velocityModel(mass)

        if (self == VELOCITY.RANDOM):
            return np.random.randint(10,30)

        if (self == VELOCITY.TAYLOR):
            return self.Taylor()











# Defining methods
    def Taylor(self):
        df = pd.read_excel('models/Distribution.xlsx', sheet_name='Sheet1', names=["velocity", "probability"])
        return choices(df["velocity"], df["probability"])[0]


    def velocityModel(self, mass):
        if (mass > 10 ** (-6)):
            return 11
        if (10 ** (-16) < mass <= 10 ** (-6)):
            # return self.__line(10**-16, 20, 10**-9, 7, mass) #Choose interpolation: self.__line -> linear;
            return self.__logline(10 ** -16, 30, 10 ** -6, 11, mass)  # self.__log -> logaritmic
        if (mass <= 10 ** (-16)):
            return 30
        return None

    # Returns the Y value of the function Y = f(X), where f(X) is the straight line through (x1,y1) and (x2,y2)
    def __line(self, x1, y1, x2, y2, X):
        a = (y2 - y1) / (x2 - x1)
        return a * (X - x1) + y1

    # Returns the Y value of the function Y = f(X), where f(X) is the straight line through (log(x1),y1) and (log(x2),y2)
    def __logline(self, x1, y1, x2, y2, X):
        a = (y2 - y1) / np.log(x2 / x1)
        return a * np.log(X / x1) + y1