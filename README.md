![Logo](path_to_the_logo/logo.jpeg)  

# Dark Plotter

Dark Plotter is a Python package for visualizing velocity as a function of radius for the Milky Way galaxy in an interactive way. This Python package was developed as a project for the Code/Astro workshop in 2024. [Code/Astro 2024](https://github.com/semaphoreP/codeastro)

The study of the orbital velocity of the galactic disk has provided astronomers with insights into the nature of dark matter, a substance that is so far not well understood, despite composing approximately one-third of the universal energy density. The equations of gravity, both classic and relativistic, fail to explain why galactic rotation curves do not decay as quickly as we expect they should with increasing distance from the core. Mathematical models to describe the gravitational potential profiles for galaxies as a function of radius, including the Navarro-Frenk-White, Plummer, Hernquist, and Jaffe profiles offer different perspectives on a galaxy's mass and velocity distribution. However, researchers and students often face challenges in visualizing and comparing these models with observed data, emphasizing the need for an interactive tool to aid in the teaching and exploration of galactic dynamics. This tool enables the direct comparison of the observed Milky Way velocity profile with the specified models. 

# Attribution
If you use this code in your research work, please refer to the package by its name and cite the authors! If you have any questions, feel free to open an issue through GitHub.

# Dependencies and Installation

This repository requires Python 3.10 or newer, and a list of packages downloaded automatically ([numpy](https://github.com/numpy/numpy), [scipy](https://scipy.org/), etc.). In addition, it is required to install all the dependencies related to [plotly](https://plotly.com/python/).

# Installation

You can install **Dark Plotter** on Windows, MacOS, and Linux distributions. In either case, we assume that you have already installed the dependencies and the appropriate Python version. There are two options to install **Dark Plotter**:

## GitHub

You can install the latest sources from **Dark Plotter** by cloning the repository directly from GitHub:
```
$ git clone https://github.com/brettonsimpson/group-13
$ cd Dark Plotter
$ pip install INSERT PIP INSTALL IDENTIFIER
```
Or, instead, use `pip` with the path to the repository:
```
$ pip install Dark Plotter@git+https://github.com/brettonsimpson/group-13
```

## PyPI
A stable compiled version of **Dark Plotter** is available on [PyPI](https://pypi.org/). You can install it by running:
```
$ pip install Dark Plotter
```

## Testing

If you have installed the development version of **Dark Plotter** or cloned the complete source code (e.g., from the GitHub repository), you can run the tests by executing the following commands:

```
$ cd Dark Plotter
$ python -m unittest -v
```
