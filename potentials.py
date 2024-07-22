import numpy as np
import plotly.graph_objs as go
from ipywidgets import interact, FloatSlider
import astropy.constants as c
from scipy import special

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

class IsothermalPotential(Potential):
    """
    Class for Isothermal gravitational potential.

    Attributes:
        sigma (float): Velocity dispersion in m/s.
    """
    
    def __init__(self, r, sigma):
        """
        Initializes the IsothermalPotential class.

        Parameters:
            r (ndarray): Radial distance array in meters.
            sigma (float): Velocity dispersion in km/s.
        """
        super().__init__(r)
        self.sigma = sigma * 1e3  # Convert km/s to m/s

    def potential(self):
        """
        Computes the Isothermal gravitational potential.

        Returns:
            phi (ndarray): Gravitational potential array.
        """
        return self.sigma**2 * np.log(self.r)

    def rotation_curve(self):
        """
        Computes the rotation curve for the isothermal potential.

        Returns:
            v_c (ndarray): Rotation velocity array in m/s.
        """
        return np.sqrt(2) * self.sigma * np.ones_like(self.r)

# Load the observational data from MWay.dat
data = np.loadtxt("MWay.dat", skiprows=1)
r_obs = data[:, 0] # Distance in kpc
v_obs = data[:, 1] # Velocity in km/s
sigma_obs = data[:, 2] # Uncertainty in km/s

# Functions to fit the potentials to the Velocity Curve
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
def update_plot(a_nfw, a_hernquist, a_plummer, a_jaffe, sigma_iso):
    nfw = NFWPotential(r, a_nfw)
    hernquist = HernquistPotential(r, a_hernquist)
    plummer = PlummerPotential(r, a_plummer)
    jaffe = JaffePotential(r, a_jaffe)
    isothermal = IsothermalPotential(r, sigma_iso)

    v_nfw = nfw.rotation_curve()
    v_hernquist = hernquist.rotation_curve()
    v_plummer = plummer.rotation_curve()
    v_jaffe = jaffe.rotation_curve()
    v_isothermal = isothermal.rotation_curve()

    # Plot the results
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_nfw / 1e3, mode='lines', name='NFW'))
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_hernquist / 1e3, mode='lines', name='Hernquist'))
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_plummer / 1e3, mode='lines', name='Plummer'))
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_jaffe / 1e3, mode='lines', name='Jaffe'))
    fig.add_trace(go.Scatter(x=r / 3.086e19, y=v_isothermal / 1e3, mode='lines', name='Isothermal'))
    fig.add_trace(go.Scatter(x=r_obs / 3.086e19, y=v_obs / 1e3, mode='markers', name='Observations',
                             error_y=dict(type='data', array=sigma_obs / 1e3, arrayminus=sigma_obs / 1e3)))

    fig.update_layout(title='Rotation Curves', xaxis_title='Distance (kpc)', yaxis_title='Velocity (km/s)')
    fig.show()

# Interactive widgets
interact(update_plot,
         a_nfw=FloatSlider(min=1, max=100, step=1, value=20, description='NFW scale radius (kpc)'),
         a_hernquist=FloatSlider(min=1, max=100, step=1, value=20, description='Hernquist scale radius (kpc)'),
         a_plummer=FloatSlider(min=1, max=100, step=1, value=20, description='Plummer scale radius (kpc)'),
         a_jaffe=FloatSlider(min=1, max=100, step=1, value=20, description='Jaffe scale radius (kpc)'),
         sigma_iso=FloatSlider(min=10, max=300, step=10, value=100, description='Isothermal velocity dispersion (km/s)'))
