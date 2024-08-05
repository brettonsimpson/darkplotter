import numpy as np
import plotly.graph_objs as go
from ipywidgets import interact, FloatSlider, Checkbox, HBox, VBox
import plotly.graph_objs as go
import ipywidgets as widgets
import astropy.constants as c
import os


# Define the radial distance array in meters
r = np.linspace(0.1, 50, 500) * 3.086e19  # Convert kpc to meters

# Constants in SI units
G = c.G.value  # Gravitational constant in m^3 kg^-1 s^-1
M = 1.5e12 * c.M_sun.value  # Galaxy mass in kg, assumed constant

class Potential:
    """
    Base class for gravitational potential.

    Attributes:
        r (ndarray): Radial distance array in meters.
    """

    def __init__(self, r):
        """
        Initializes the Potential class.

        Parameters:
            r (ndarray): Radial distance array in meters.
        """
        self.r = r

    def potential(self):
        """
        Computes the gravitational potential.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def rotation_curve(self):
        """
        Computes the rotation curve from the gravitational potential.

        Returns:
            v_c (ndarray): Rotation velocity array in m/s.
        """
        dPhi_dr = np.gradient(self.potential(), self.r)
        v_c = np.sqrt(self.r * np.abs(dPhi_dr))  # in m/s
        return v_c

class NFWPotential(Potential):
    """
    Class for Navarro-Frenk-White (NFW) gravitational potential.

    Attributes:
        a (float): Scale radius in meters.
    """
    
    def __init__(self, r, a):
        """
        Initializes the NFWPotential class.

        Parameters:
            r (ndarray): Radial distance array in meters.
            a (float): Scale radius in kpc.
        """
        super().__init__(r)
        self.a = a * 3.086e19  # Convert kpc to meters

    def potential(self):
        """
        Computes the NFW gravitational potential.

        Returns:
            phi (ndarray): Gravitational potential array.
        """
        return - G * M / self.r * np.log(1 + self.r / self.a)

class HernquistPotential(Potential):
    """
    Class for Hernquist gravitational potential.

    Attributes:
        a (float): Scale radius in meters.
    """

    def __init__(self, r, a):
        """
        Initializes the HernquistPotential class.

        Parameters:
            r (ndarray): Radial distance array in meters.
            a (float): Scale radius in kpc.
        """
        super().__init__(r)
        self.a = a * 3.086e19  # Convert kpc to meters

    def potential(self):
        """
        Computes the Hernquist gravitational potential.

        Returns:
            phi (ndarray): Gravitational potential array.
        """
        return - G * M / (self.r + self.a)

class PlummerPotential(Potential):
    """
    Class for Plummer gravitational potential.

    Attributes:
        a (float): Scale radius in meters.
    """

    def __init__(self, r, a):
        """
        Initializes the PlummerPotential class.

        Parameters:
            r (ndarray): Radial distance array in meters.
            a (float): Scale radius in kpc.
        """
        super().__init__(r)
        self.a = a * 3.086e19  # Convert kpc to meters

    def potential(self):
        """
        Computes the Plummer gravitational potential.

        Returns:
            phi (ndarray): Gravitational potential array.
        """
        return - G * M / np.sqrt(self.r**2 + self.a**2)

class JaffePotential(Potential):
    """
    Class for Jaffe gravitational potential.

    Attributes:
        a (float): Scale radius in meters.
    """
    
    def __init__(self, r, a):
        """
        Initializes the JaffePotential class.

        Parameters:
            r (ndarray): Radial distance array in meters.
            a (float): Scale radius in kpc.
        """
        super().__init__(r)
        self.a = a * 3.086e19  # Convert kpc to meters

    def potential(self):
        """
        Computes the Jaffe gravitational potential.

        Returns:
            phi (ndarray): Gravitational potential array.
        """
        return - G * M / self.a * np.log(1 + self.a / self.r)

data_path = os.path.join(os.path.dirname(__file__), 'MW_Vc.txt')

data = np.loadtxt(data_path, skiprows=2)
r_obs = data[:, 0] * 3.086e19  # Distance in meters (converted from kpc)
v_obs = data[:, 1] * 1e3  # Velocity in meters per second (converted from km/s)
sigma_plus = data[:, 2] * 1e3  # Positive uncertainty in meters per second (converted from km/s)
sigma_minus = data[:, 3] * 1e3  # Negative uncertainty in meters per second (converted from km/s)

