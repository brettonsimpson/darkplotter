import numpy as np

class Potential:
    def __init__(self, r):
        self.r = r

    def potential(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def rotation_curve(self):
        return np.sqrt(self.r * np.abs(self.potential()))

class NFWPotential(Potential):
    def __init__(self, r, rho_s, r_s):
        super().__init__(r)
        self.rho_s = rho_s
        self.r_s = r_s

    def potential(self):
        x = self.r / self.r_s
        return -4 * np.pi * self.rho_s * self.r_s**3 * (np.log(1 + x) - x / (1 + x)) / self.r

class ExponentialPotential(Potential):
    def __init__(self, r, sigma_0, r_d):
        super().__init__(r)
        self.sigma_0 = sigma_0
        self.r_d = r_d

    def potential(self):
        return -4 * np.pi * self.sigma_0 * self.r_d * (1 - np.exp(-self.r / self.r_d))
