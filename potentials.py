import numpy as np

def plummer_sphere_potential(radius, z, b, amplitude):
    return -amplitude/np.sqrt(radius**2 + z**2 + b**2)

def NFW_potential(radius, a, amplitude):
    first_term = amplitude/4*np.pi*a**3
    second_term = ((radius/a)*(1+radius/a)**2)**-1
    return first_term*second_term