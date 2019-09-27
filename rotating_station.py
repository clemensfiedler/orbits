"""Simulates a rotating station
"""

# imports
import numpy as np
from scipy import integrate

from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames

# model setup
radius = 10
sec_per_rotation = 10
boundary_speed = 2*np.pi*radius / sec_per_rotation
pos_init = 0

# simulation
dt = 0.01
n_times = 2000
sim_speed = 100

# setup figure:
fig = plt.figure()
ax = plt.gca()

ax.set_xlim(-radius*2, +radius*2)
ax.set_ylim(-radius*2, +radius*2)
ax.set_aspect(aspect=1.0)

ax.plot(0,0,'x', color='k')
station = plt.Circle((0, 0), radius, color='k', fill=False)
ax.add_artist(station)

# animate
def init():
    """initialize starting postion
    """
    pos = pos_init
    x = np.array((np.cos(pos)*radius, np.sin(pos)*radius))
    v = np.array((-np.sin(pos)*radius, np.cos(pos)*radius))

    point, = ax.plot(*x, 'x', lw=2, color='C0')
    speed = ax.annotate("", xy=(x+v), xytext=x,
        arrowprops=dict(arrowstyle="->", color = 'C2'))
    centrif = ax.annotate("", xy=(x+x/sec_per_rotation*2), xytext=x, 
        arrowprops=dict(arrowstyle="->", color='C1'))

    return point, speed, centrif

def update(frame):
    """update postion
    """
    pos = pos_init + frame*dt

    x = np.array((np.cos(pos)*radius, np.sin(pos)*radius))
    v = np.array((-np.sin(pos)*radius, np.cos(pos)*radius))

    point, = ax.plot(*x, 'x', lw=2, color='C0')
    speed = ax.annotate("", xy=(x+v), xytext=x, 
        arrowprops=dict(arrowstyle="->", color='C2'))
    centrif = ax.annotate("", xy=(x+x/sec_per_rotation*2), xytext=x, 
        arrowprops=dict(arrowstyle="->", color='C1'))

    return point, speed, centrif

# do the actual animation
animate = FuncAnimation(fig, update, frames=np.arange(1, n_times, 1), 
                    init_func=init, blit=True, interval=10)
plt.show()