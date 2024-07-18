import numpy as np
import plotly.graph_objs as go
from ipywidgets import interact, FloatSlider, Checkbox, HBox, VBox
import plotly.graph_objs as go
import ipywidgets as widgets

from potentials import *

# Create initial figure widget



def plot(potential):

    if potential == "all":

        r = np.linspace(0.1, 50, 100)  # Avoiding r=0 to prevent singularity



        fig = go.FigureWidget()
        fig.update_layout(title="Rotation Curves", xaxis_title="Radial Distance (r)", yaxis_title="Rotation Curve (v)", height=500, width=800)

        # Function to update the plot
        def update_plot(r_s=1, r_d=1, show_nfw= True, show_exponential=True): # default values
            with fig.batch_update():
                fig.data = []  # Clear existing data

                if show_nfw:
                    nfw_potential = NFWPotential(r, r_s)
                    nfw_curve = nfw_potential.rotation_curve()
                    fig.add_trace(go.Scatter(x=r, y=nfw_curve, name='NFW'))
                

                if show_exponential:
                    exp_potential = ExponentialPotential(r, r_d)
                    exp_curve = exp_potential.rotation_curve()
                    fig.add_trace(go.Scatter(x=r, y=exp_curve, name='Exponential'))


        # Create interactive sliders and checkboxes
        r_s_slider = FloatSlider(min=1, max=20, step=0.1, value=1, description='r_s')
        r_d_slider = FloatSlider(min=1, max=20, step=0.01, value=1, description='r_d')

        show_nfw_checkbox = Checkbox(value=True, description='Show NFW')
        show_exponential_checkbox = Checkbox(value=True, description='Show Exponential')

        # Link interactive controls to update function
        interactive_controls = widgets.interactive(update_plot, 
                                                r_s=r_s_slider, 
                                                r_d=r_d_slider, 
                                                show_nfw=show_nfw_checkbox, 
                                                show_exponential=show_exponential_checkbox)

        # Display the interactive controls and figure
        ui = VBox([HBox([r_s_slider]), HBox([r_d_slider]), HBox([show_nfw_checkbox, show_exponential_checkbox])])
        display(ui, fig)

        # Initial plot update
    update_plot(r_s=11, r_d=1, show_nfw=True, show_exponential=True)

