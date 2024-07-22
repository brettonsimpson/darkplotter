import numpy as np
import plotly.graph_objs as go
from ipywidgets import interact, FloatSlider, Checkbox, HBox, VBox, Button, Text, Output
from IPython.display import display
import plotly.graph_objs as go
import ipywidgets as widgets
import astropy.constants as c

from potentials import *

# Create initial figure widget


    
def plot():
    
# Create initial figure widget
    fig = go.FigureWidget()
    fig.update_layout(title="Galactic Rotation Curves", 
                    xaxis_title="Radial Distance (kpc)", 
                    yaxis_title="Rotation Velocity (km/s)", 
                    height=500, width=800)

    # Function to create the plot
    def update_plot(a_nfw=10, a_hernquist=10, a_plummer=10, a_jaffe=10, show_nfw=True, show_hernquist=True, show_plummer=True, show_jaffe=True):
        with fig.batch_update():
            fig.data = []  # Clear existing data

            if show_nfw:
                nfw_potential = NFWPotential(r, a_nfw)
                nfw_curve = nfw_potential.rotation_curve()
                fig.add_trace(go.Scatter(x=r / 3.086e19, y=nfw_curve / 1e3, name='NFW'))  # Convert r to kpc and v to km/s

            if show_hernquist:
                hernquist_potential = HernquistPotential(r, a_hernquist)
                hernquist_curve = hernquist_potential.rotation_curve()
                fig.add_trace(go.Scatter(x=r / 3.086e19, y=hernquist_curve / 1e3, name='Hernquist'))  # Convert r to kpc and v to km/s

            if show_plummer:
                plummer_potential = PlummerPotential(r, a_plummer)
                plummer_curve = plummer_potential.rotation_curve()
                fig.add_trace(go.Scatter(x=r / 3.086e19, y=plummer_curve / 1e3, name='Plummer'))  # Convert r to kpc and v to km/s

            if show_jaffe:
                jaffe_potential = JaffePotential(r, a_jaffe)
                jaffe_curve = jaffe_potential.rotation_curve()
                fig.add_trace(go.Scatter(x=r / 3.086e19, y=jaffe_curve / 1e3, name='Jaffe'))  # Convert r to kpc and v to km/s

            # Add experimental data points with error bars
            fig.add_trace(go.Scatter(
                x=r_obs / 3.086e19, y=v_obs / 1e3,  # Convert r to kpc and v to km/s
                mode='markers', 
                name='Observational Data', 
                error_y=dict(
                    type='data',
                    symmetric=False,
                    array=sigma_plus / 1e3,  # Convert to km/s
                    arrayminus=sigma_minus / 1e3  # Convert to km/s
                )
            ))

    # Create interactive sliders and checkboxes
    a_nfw_slider = FloatSlider(min=1, max=30, step=0.1, value=10, description='a (NFW) kpc')
    a_hernquist_slider = FloatSlider(min=1, max=30, step=0.1, value=10, description='a (Hernquist) kpc')
    a_plummer_slider = FloatSlider(min=1, max=30, step=0.1, value=10, description='a (Plummer) kpc')
    a_jaffe_slider = FloatSlider(min=1, max=30, step=0.1, value=10, description='a (Jaffe) kpc')

    show_nfw_checkbox = Checkbox(value=True, description='Show NFW')
    show_hernquist_checkbox = Checkbox(value=True, description='Show Hernquist')
    show_plummer_checkbox = Checkbox(value=True, description='Show Plummer')
    show_jaffe_checkbox = Checkbox(value=True, description='Show Jaffe')

    # Create input boxes for parameter values
    a_nfw_input = Text(value='10', description='a (NFW):')
    a_hernquist_input = Text(value='10', description='a (Hernquist):')
    a_plummer_input = Text(value='10', description='a (Plummer):')
    a_jaffe_input = Text(value='10', description='a (Jaffe):')
    error_message = Output()

    def update_sliders(*args):
        try:
            if show_nfw_checkbox.value:
                a_nfw_value = float(a_nfw_input.value)
                if not (0 <= a_nfw_value <= 30):
                    raise ValueError('a (NFW) must be between 0 and 30.')
                a_nfw_slider.value = a_nfw_value

            if show_hernquist_checkbox.value:
                a_hernquist_value = float(a_hernquist_input.value)
                if not (0 <= a_hernquist_value <= 30):
                    raise ValueError('a (Hernquist) must be between 0 and 30.')
                a_hernquist_slider.value = a_hernquist_value

            if show_plummer_checkbox.value:
                a_plummer_value = float(a_plummer_input.value)
                if not (0 <= a_plummer_value <= 30):
                    raise ValueError('a (Plummer) must be between 0 and 30.')
                a_plummer_slider.value = a_plummer_value

            if show_jaffe_checkbox.value:
                a_jaffe_value = float(a_jaffe_input.value)
                if not (0 <= a_jaffe_value <= 30):
                    raise ValueError('a (Jaffe) must be between 0 and 30.')
                a_jaffe_slider.value = a_jaffe_value

            with error_message:
                error_message.clear_output()

        except ValueError as e:
            with error_message:
                error_message.clear_output()
                print(f"Error: {e}")

    # Link input boxes to slider update function
    a_nfw_input.observe(update_sliders, 'value')
    a_hernquist_input.observe(update_sliders, 'value')
    a_plummer_input.observe(update_sliders, 'value')
    a_jaffe_input.observe(update_sliders, 'value')

    # Button to save the current plot configuration
    save_button = Button(description='Save Plot')
    output = Output()

    def save_plot(b):
        with output:
            fig.write_image(f"plot_{a_nfw_slider.value}_{a_hernquist_slider.value}_{a_plummer_slider.value}_{a_jaffe_slider.value}.png")
            print(f"Plot saved as curve_{a_nfw_slider.value}_{a_hernquist_slider.value}_{a_plummer_slider.value}_{a_jaffe_slider.value}.png")

    save_button.on_click(save_plot)

    # Link interactive controls to update function
    interactive_controls = widgets.interactive(update_plot, 
                                            a_nfw=a_nfw_slider, 
                                            a_hernquist=a_hernquist_slider, 
                                            a_plummer=a_plummer_slider, 
                                            a_jaffe=a_jaffe_slider, 
                                            show_nfw=show_nfw_checkbox, 
                                            show_hernquist=show_hernquist_checkbox, 
                                            show_plummer=show_plummer_checkbox, 
                                            show_jaffe=show_jaffe_checkbox)

    # Display the interactive controls and figure
    ui = VBox([
        HBox([a_nfw_slider, a_hernquist_slider, a_plummer_slider, a_jaffe_slider]), 
        HBox([show_nfw_checkbox, show_hernquist_checkbox, show_plummer_checkbox, show_jaffe_checkbox]),
        HBox([a_nfw_input, a_hernquist_input, a_plummer_input, a_jaffe_input]),
        error_message,
        save_button,
        output
    ])
    display(ui, fig)

    # Initial plot update
    update_plot()