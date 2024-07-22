import numpy as np
import plotly.graph_objs as go
from ipywidgets import interact, FloatSlider, Checkbox, HBox, VBox
import plotly.graph_objs as go
import ipywidgets as widgets
import astropy.constants as c
from scipy import special
from astropy.io import ascii
import scipy.optimize as op

# Define the radial distance array in meters
r = np.linspace(0.1, 50, 500) * 3.086e19  # Convert kpc to meters

# Constants in SI units
G = c.G.value  # Gravitational constant in m^3 kg^-1 s^-1
M = 1.5e12 * c.M_sun.value  # Galaxy mass in kg, assumed constant
G_astro = 4.302e-6

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

# Load the observational data
data = np.loadtxt("MW_Vc.txt", skiprows=2)
r_obs = data[:, 0] * 3.086e19  # Distance in meters (converted from kpc)
v_obs = data[:, 1] * 1e3  # Velocity in meters per second (converted from km/s)
sigma_plus = data[:, 2] * 1e3  # Positive uncertainty in meters per second (converted from km/s)
sigma_minus = data[:, 3] * 1e3  # Negative uncertainty in meters per second (converted from km/s)

# Functions if we'd like to fit the potentials and find the value parameters
Y_plummer = lambda x, b, M: ((G_astro * M) / (x**2. + b**2.)**1.5)**.5 * x
Y_Kuzmin = lambda x, a, M: ((((G_astro) * (M))**.5) / ((x**2. + a**2.)**0.75)) * x
Y_exponencial = lambda x, rd, s: ((np.pi * G_astro * (s) * (x**2.) / (rd)) * (((special.iv(0, x / (2. * rd))) * (special.kn(0, x / (2. * rd)))) - ((special.iv(1, x / (2. * rd))) * (special.kn(1, x / (2. * rd))))))**.5
Y_NFW = lambda x, a1, ro: (-4. * np.pi * G_astro * ro * (a1**3.) * (x - (a1 + x) * np.log(1. + (x / a1))) / (x * (a1 + x)))**.5
Y_isothermal = lambda x, sigma: np.sqrt(2.) * sigma * (x / x)

def chi_plum(params, x, y, yerr):
    b = params[0]
    M = 10**params[1]
    def velocidad(xx):
        return Y_plummer(xx, b, M)
    modelo = velocidad(x)
    result = sum((y - modelo)**2. / yerr**2.)
    return result

def chi_kuz(params, x, y, yerr):
    a = params[0]
    M = 10**params[1]
    def velocidad(xx):
        return Y_Kuzmin(xx, a, M)
    modelo = velocidad(x)
    result = sum((y - modelo)**2. / yerr**2.)
    return result

def chi_exp(params, x, y, yerr):
    rd = params[0]
    s = 10**params[1]
    def velocidad(xx):
        return Y_exponencial(xx, rd, s)
    modelo = velocidad(x)
    result = sum((y - modelo)**2. / yerr**2.)
    return result

def chi_NFW(params, x, y, yerr):
    a1 = 10**params[0]
    ro = 10**params[1]
    def velocidad(xx):
        return Y_NFW(xx, a1, ro)
    modelo = velocidad(x)
    result = sum((y - modelo)**2. / yerr**2.)
    return result

def chi_iso(params, x, y, yerr):
    sigma = 10**params[0]
    def velocidad(xx):
        return Y_isothermal(xx, sigma)
    modelo = velocidad(xx)
    result = sum((y - modelo)**2. / yerr**2.)
    return result

# Interactive plotting
def update_plot(a_nfw, a_hernquist, a_plummer, a_jaffe):
    # Create potential instances
    nfw = NFWPotential(r, a_nfw)
    hernquist = HernquistPotential(r, a_hernquist)
    plummer = PlummerPotential(r, a_plummer)
    jaffe = JaffePotential(r, a_jaffe)
    
    # Compute rotation curves
    v_nfw = nfw.rotation_curve()
    v_hernquist = hernquist.rotation_curve()
    v_plummer = plummer.rotation_curve()
    v_jaffe = jaffe.rotation_curve()

    # Plot the results
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_nfw / 1e3, mode='lines', name='NFW'))
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_hernquist / 1e3, mode='lines', name='Hernquist'))
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_plummer / 1e3, mode='lines', name='Plummer'))
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_jaffe / 1e3, mode='lines', name='Jaffe'))
    fig.add_trace(go.Scatter(x=r_obs / 3.086e19, y=v_obs / 1e3, mode='markers', name='Observations',
                             error_y=dict(type='data', array=sigma_plus / 1e3, arrayminus=sigma_minus / 1e3)))

    fig.update_layout(title='Rotation Curves', xaxis_title='Distance (kpc)', yaxis_title='Velocity (km/s)')
    fig.show()

# Interactive widgets
interact(update_plot,
         a_nfw=FloatSlider(min=1, max=100, step=1, value=20, description='NFW scale radius (kpc)'),
         a_hernquist=FloatSlider(min=1, max=100, step=1, value=20, description='Hernquist scale radius (kpc)'),
         a_plummer=FloatSlider(min=1, max=100, step=1, value=20, description='Plummer scale radius (kpc)'),
         a_jaffe=FloatSlider(min=1, max=100, step=1, value=20, description='Jaffe scale radius (kpc)'))
