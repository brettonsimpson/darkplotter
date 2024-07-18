![Logo](path_to_the_logo/logo.jpeg)  

# group-13 Project

**Package name** is a Python 3 package to visualize the orbital radius for the Milky Way galaxy, in an interacting way. It is distributed over the MIT License. This Python package is associated with the main activites of [Code/Astro 2024](https://github.com/semaphoreP/codeastro).

# Statement of need
Understanding the dynamics and structure of the Milky Way galaxy is a fundamental goal in astrophysics. A critical aspect of this is analyzing the rotation curve, which represents the orbital velocity of stars and gas as a function of their distance from the galactic center. Discrepancies between observed rotation curves and those predicted by visible matter alone have led to the hypothesis of dark matter, necessitating more sophisticated models. Traditional models like the Triaxial NFW Potential, Plummer Potential, and Exponential Potential offer different perspectives on the galaxy's mass distribution. However, researchers and students often face challenges in visualizing and comparing these models with observed data, highlighting the need for an intuitive, interactive tool to aid in the exploration and understanding of galactic dynamics.

Our Python package addresses this need by providing an interactive platform to visualize and analyze the orbital radius as a function of velocity for the Milky Way galaxy. Users can adjust parameters for the Triaxial NFW, Plummer, and Exponential potentials to see how each model affects the simulated velocity profile. This tool allows for direct comparison with observed velocity profiles, facilitating a deeper understanding of galactic dynamics and the influence of different mass distribution models. By making these complex models accessible and manipulatable, our package serves as an additional resource for both educational and research purposes in astrophysics.

# Attribution
If you use this code in your research work, please refer to the package by its name and cite the authors!. If you have any questions, feel free to open an issue through GitHub.

# Dependencies and Installation

This repository requires Python 3.10 or high, and a list of packages downloaded automatically ([numpy](https://github.com/numpy/numpy), [scipy](https://scipy.org/), etc.). In addition, it is required to install all the dependencies related to [plotly](https://plotly.com/python/).

# Installing **Package_Name**

You can install **Package_Name** on Windows, MacOS, and Linux distributions. In either case, we assume that you have already installed the dependencies and the appropriate Python version. There are two options to install **Package_Name**:

## GitHub

You can install the latest sources from **Package_Name** by cloning the repository directly from GitHub:
```
$ git clone https://github.com/brettonsimpson/group-13
$ cd package_name
$ pip install .
```
Or, instead, use `pip` with the path to the repository:
```
$ pip install package_name@git+https://github.com/brettonsimpson/group-13
```

## PyPI
A stable compiled version of **Package_Name** is available on [PyPI](https://pypi.org/). You can install it by running:
```
$ pip install package_name
```

## Testing

If you have installed the development version of **Package_Name** or cloned the complete source code (e.g., from the GitHub repository), you can run the tests by executing the following commands:

```
$ cd package_name
$ python -m unittest -v
```
