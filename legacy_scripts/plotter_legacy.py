import numpy as np
import matplotlib.pyplot as plt
from potentials import plummer_sphere_potential
from potentials import NFW_potential

radii = np.linspace(0, int(1e1), int(1e2))
amplitude = 5
b = 0.22
z = 2
a = 3

plt.plot(plummer_sphere_potential(radii, z, b, amplitude), color = 'b', label = 'Plummer Sphere Potential')
plt.plot(NFW_potential(radii, a, amplitude), color = 'r', label = 'NFW Potential')
plt.xlabel('Radius')
plt.ylabel('Potential')
plt.legend()
plt.show()