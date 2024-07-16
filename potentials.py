import numpy as np
import astropy.constants as c

def plummer_sphere_potential(radius, z, b, amplitude):
    return -amplitude/np.sqrt(radius**2 + z**2 + b**2)

def NFW_potential(radius_array, radius, initial_mass):
    return -(4*np.pi*c.G*radius**3/radius_array)/np.log(1+radius_array/radius)