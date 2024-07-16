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

import plotly.graph_objs as go
from plotly.subplots import make_subplots
from ipywidgets import interact, FloatSlider

# Define the radial distance array
r = np.linspace(0.1, 50, 500)  # Avoiding r=0 to prevent singularity

def update_plot(rho_s=0.01, r_s=10, sigma_0=0.01, r_d=5):
    # Create NFW Potential
    nfw_potential = NFWPotential(r, rho_s, r_s)
    nfw_curve = nfw_potential.rotation_curve()

    # Create Exponential Potential
    exp_potential = ExponentialPotential(r, sigma_0, r_d)
    exp_curve = exp_potential.rotation_curve()

    # Create the plot
    fig = make_subplots(rows=1, cols=2, subplot_titles=('NFW Potential', 'Exponential Potential'))

    fig.add_trace(go.Scatter(x=r, y=nfw_curve, mode='lines', name='NFW'), row=1, col=1)
    fig.add_trace(go.Scatter(x=r, y=exp_curve, mode='lines', name='Exponential'), row=1, col=2)

    fig.update_layout(height=500, width=1000, title_text="Rotation Curves")
    fig.show()

# Create interactive sliders
interact(update_plot, rho_s=FloatSlider(min=0.001, max=0.1, step=0.001, value=0.01),
                     r_s=FloatSlider(min=1, max=20, step=0.1, value=10),
                     sigma_0=FloatSlider(min=0.001, max=0.1, step=0.001, value=0.01),
                     r_d=FloatSlider(min=1, max=20, step=0.1, value=5))
