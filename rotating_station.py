"""Simulates a rotating station
"""

# imports
import numpy as np
from scipy import integrate

from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames

def norm(v):
    """normalizes vector to have unit length"""
    v_norm = v/np.sqrt(sum(v**2))
    return v_norm

# simulation parameters
dt = 0.01
n_times = 2000
sim_speed = 1

# model parameters
radius = 500 #radius in meters
sec_per_rotation = 10 #seconds per rotation
v_rot = 2*np.pi*radius/sec_per_rotation #surface speed in m/s
pos_init = 0
jump = v_rot-50 #delta v of jump in m/s

# basic calculations
x_init = np.array((np.cos(pos_init), np.sin(pos_init)))*radius
v_init = np.array((-np.sin(pos_init), np.cos(pos_init)))*v_rot
v_jump = v_init - x_init/(np.sqrt(sum(x_init**2)))*jump
v_jump_norm = norm(v_jump)

# calculate the intersection
cos_th = np.inner(norm(v_init),norm(v_jump))
cos_th2 = np.cos(2*np.arccos(cos_th))
cord_len = radius*np.sqrt(2-2*cos_th2)
t_jump = cord_len/np.sqrt(sum(v_jump**2))

# setup figure:
fig = plt.figure()
ax = plt.gca()

ax.set_xlim(-radius*2, +radius*2)
ax.set_ylim(-radius*2, +radius*2)
ax.set_aspect(aspect=1.0)

ax.plot(0,0,'x', color='k')
station = plt.Circle((0, 0), radius, color='k', fill=False)
ax.add_artist(station)

ax.plot([x_init[0],x_init[0]+v_jump_norm[0]*cord_len],
        [x_init[1],x_init[1]+v_jump_norm[1]*cord_len],
        '-', lw=1, color='grey')

description = u'radius: {:.2f}m\nrotation time {:.2f}s\nspeed:{:.2f}$m/s$\njump $\Delta v$: {:.2f}$m/s$\njump duration: {:.2f}s\nsimulation speed: {}'.format(radius, sec_per_rotation, v_rot, jump, t_jump, dt*sim_speed)
print(description)

# animate
def init():
    """initialize starting postion
    """
    point, = ax.plot(*x_init, 'x', lw=2, color='C0')
    speed = ax.annotate("", xy=(x_init+v_init*dt), xytext=x_init,
        arrowprops=dict(arrowstyle="->", color = 'C2'))
    centrif = ax.annotate("", xy=(x_init+x_init/sec_per_rotation*2),
        xytext=x_init, 
        arrowprops=dict(arrowstyle="->", color='C1'))

    point_jump, = ax.plot(*x_init, 'x', lw=2, color='C3')

    text = ax.text(-radius*1.9,radius*1.9,description, 
    verticalalignment='top', fontsize=8)

    time = ax.text(radius*1.9,radius*1.9, 'time:' + str(0), 
    verticalalignment='top', fontsize=8)

    # path = ax.plot(None, None, '-', c = 'k')

    return point, speed, centrif, point_jump, time

def update(frame):
    """update postion
    """
    global v_jump

    t = frame
    t = min(frame, t_jump/dt)
    # t = min(frame, sec_per_rotation/dt)

    pos = pos_init + t*dt/sec_per_rotation*2*np.pi

    x = np.array((np.cos(pos), np.sin(pos)))*radius
    v = np.array((-np.sin(pos), np.cos(pos)))

    point, = ax.plot(*x, 'x', lw=2, color='C0')
    speed = ax.annotate("", xy=(x+v*v_rot), xytext=x,
        arrowprops=dict(arrowstyle="->", color='C2'))
    centrif = ax.annotate("", xy=(x+x/sec_per_rotation*2), xytext=x, 
        arrowprops=dict(arrowstyle="->", color='C1'))

    point_jump, = ax.plot(*(x_init+v_jump*dt*t) , 'x', lw=2, color='C3')
    time = ax.text(radius*1.9,radius*1.9, 'time:{:.2f}s'.format(t*dt), 
    verticalalignment='top', ha='right', fontsize=8)

    return point, speed, centrif, point_jump, time

# do the actual animation
animate = FuncAnimation(fig, update, frames=np.arange(1, n_times, 1), 
                    init_func=init, blit=True, interval=dt*1000/sim_speed)
plt.show()