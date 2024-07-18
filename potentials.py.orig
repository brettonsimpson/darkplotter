import numpy as np
import plotly.graph_objs as go
from ipywidgets import interact, FloatSlider, Checkbox, HBox, VBox
import plotly.graph_objs as go
import ipywidgets as widgets

# Define the radial distance array
r = np.linspace(0.1, 50, 500)  # Avoiding r=0 to prevent singularity

norm = 1. # Normalization factor


# Rotation Curve Class
class Potential:
    """
    Base class for different potential models.
    
    Attributes:
    r (numpy.ndarray): Array of radial distances.
    """
    def __init__(self, r):
        """
        Initializes the Potential with radial distances.
        
        """
        self.r = r

    def potential(self):
        """
        Computes the potential. 
        
        Returns:
        numpy.ndarray: Potential values.
        """
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def potential_derivative(self):
        """
        Computes the derivative of the potential. 
        
        Returns:
        numpy.ndarray: Derivative of potential values.
        """
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def rotation_curve(self):
        """
        Computes the rotation curve (velocity) from the potential.

        Returns:
        numpy.ndarray: Rotation curve values.
        """
        # Compute the derivative of the potential with respect to r
        dPhi_dr = np.gradient(self.potential(), self.r)
        return np.sqrt(self.r * np.abs(dPhi_dr))
    
    
# Navaro-Frenk-White (NFW) Potential
class NFWPotential(Potential):
    """
    Class for the Navarro-Frenk-White (NFW) potential.
    
    Attributes:
    r (numpy.ndarray): Array of radial distances.
    r_s (float): Scale radius for the NFW potential.
    """
    def __init__(self, r, r_s):
        """
        Initialize the NFWPotential with radial distances and scale radius.
        
        Parameters:
        r (numpy.ndarray): Array of radial distances.
        r_s (float): Scale radius for the NFW potential.
        """
        super().__init__(r)
        self.r_s = r_s

    def potential(self):
        """
        Compute the NFW potential.
        
        Returns:
        numpy.ndarray: NFW potential values.
        """
        x = self.r / self.r_s
        return norm * self.r_s**3 * (np.log(1 + x) - x / (1 + x)) / self.r
    
    # Exponential Potential
    
class ExponentialPotential(Potential):
    """
    Class for the Exponential potential.

    Attributes:
    r (numpy.ndarray): Array of radial distances.
    r_d (float): Scale radius for the Exponential potential.
    """
    def __init__(self, r, r_d):
        """
        Initialize the ExponentialPotential with radial distances and scale radius.
        
        Parameters:
        r (numpy.ndarray): Array of radial distances.
        r_d (float): Scale radius for the Exponential potential.
        """
        super().__init__(r)
        self.r_d = r_d

    def potential(self):
        """
        Compute the Exponential potential.
        
        Returns:
        numpy.ndarray: Exponential potential values.
        """
        return norm * (1 - np.exp(-self.r / self.r_d))