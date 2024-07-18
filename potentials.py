import numpy as np

norm = 1

class Potential:


    def __init__(self, r):
        self.r = r

    def potential(self):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def potential_derivative(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def rotation_curve(self):
        return np.sqrt(self.r * np.abs(self.potential())) #TBD

class NFWPotential(Potential):

    norm = 1

    def __init__(self, r, r_s):
        super().__init__(r)
        self.r_s = r_s

    def potential(self):
        norm = 1
        x = self.r / self.r_s
        return self.r_s**3 * (np.log(1 + x) - x / (1 + x)) / self.r
    
    def potential_derivative(self):
        norm = 1
        x = self.r / self.r_s
        return self.r_s**3 * (1 / (self.r * (1 + x)**2))

class ExponentialPotential(Potential):

    

    def __init__(self, r, r_d):
        super().__init__(r)
        self.r_d = r_d

    def potential(self):
        norm = 1
        return (1 - np.exp(-self.r / self.r_d))
    
    def potential_derivative(self):
        norm = 1
        return np.exp(-self.r / self.r_d)

