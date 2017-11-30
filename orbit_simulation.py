# playing around with orbital mechanics

import numpy as np
from scipy import integrate

from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames

# convert dictionary to pandas


# Model setup

# Constants:
G =  6.67e-4
dt = 0.01
n_times = 2000

# Objects
objects = {}
objects['test1'] = {'position': np.empty([n_times,3]), 'velocity': np.array([0.,0.,0.]), 'mass': 100.}
objects['test2'] = {'position': np.empty([n_times,3]), 'velocity': np.array([-1.,0.,0.]), 'mass': 10.}
objects['test3'] = {'position': np.empty([n_times,3]), 'velocity': np.array([-2.,0.0,0.0]), 'mass': 1.}
objects['test4'] = {'position': np.empty([n_times,3]), 'velocity': np.array([0,0.0,0.0]), 'mass': 1.}

objects['test1']['position'][0] = np.array([0.,0.,0.])
objects['test2']['position'][0] = np.array([0.,1.,1.])
objects['test3']['position'][0] = np.array([0.,1.1,1.1])
objects['test4']['position'][0] = np.array([0.,1.1,3.1])

n_objects = len(objects)

# Remove net momentum and average positions
avg_pos = np.zeros(3)
avg_speed = np.zeros(3)

for obj in objects:
    avg_pos   += objects[obj]['position'][0]
    avg_speed += objects[obj]['velocity']*objects[obj]['mass']


for obj in objects:
    objects[obj]['position'][0] -= avg_pos/n_objects
    objects[obj]['velocity'] -= avg_speed/(n_objects*objects[obj]['mass'] )

# Graph
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('on')

colors = plt.cm.rainbow(np.linspace(0, 1, n_objects))

xdata, ydata = [], []
point, = plt.plot([], [], 'ro', animated=True)

# Define lines and points
lines  = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
points = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])


i=0
for obj in objects:
    points[i].set_markersize(objects[obj]['mass']**(1/3))
    lines[i].set_linewidth(objects[obj]['mass']**(1/3))
    i += 1

# Define axes limits:
ax.set_xlim(-10, +10)
ax.set_ylim(-10, +10)
ax.set_zlim(-10, +10)

# text and lables
time_text = ax.text(0.02, 0.95, 0.95,'test', transform=ax.transAxes)

# Init the canvas and lines and points
def init():
    for line, pt in zip(lines, points):
        line.set_data([], [])
        line.set_3d_properties([])
        pt.set_data([], [])
        pt.set_3d_properties([])

    return lines + points

def update(frame):

    for obj1 in objects:
        g_pull = np.zeros(3)

        for obj2 in objects:
            if obj1 != obj2:
                distance = objects[obj2]['position'][frame-1] - objects[obj1]['position'][frame-1]
                if np.linalg.norm(distance)< 0.5:
                    distance =  distance / np.linalg.norm(distance)
                g_pull += distance*G*(objects[obj2]['mass'])/(np.linalg.norm(distance))**3

        objects[obj1]['velocity'] += g_pull

    i = 0

    for obj in objects:
        objects[obj]['position'][frame] = objects[obj]['position'][frame-1] + dt*objects[obj]['velocity']
        x, y, z  = objects[obj]['position'][frame]
        dx,dy,dz = objects[obj]['velocity']*10

        points[i].set_data(x, y)
        points[i].set_3d_properties(z)

        objects[obj]['position'][:frame,0]


        lines[i].set_data(objects[obj]['position'][:frame,0], objects[obj]['position'][:frame,1])
        lines[i].set_3d_properties(objects[obj]['position'][:frame,2])

        i+=1

    time_text.set_text(str(frame))

    return points+lines


animate = FuncAnimation(fig, update, frames=np.arange(1, n_times, 1),
                    init_func=init)
plt.show()

# Save as mp4. This requires mplayer or ffmpeg to be installed
#animate.save('Orbits.mp4', fps=15, extra_args=['-vcodec', 'libx264'])
