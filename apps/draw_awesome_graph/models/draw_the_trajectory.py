'''
for xy plot
Draw the trajectory of a body in projectile motion
'''


name_of_graph = 'Projectile motion of a ball'
name_of_xaxis = 'x-coordinate'
name_of_yaxis = 'y-coordinate'
symbolSize = 5

import numpy as np
import math

degree = 45
u = 40

def frange(start, final, interval):
    numbers = []
    while start < final:
        numbers.append(start)
        start = start + interval
    return numbers

theta = math.radians(degree)
g = 9.8
# Time of flight
t_flight = 2*u*math.sin(theta)/g
# find time intervals
intervals = frange(0, t_flight, 0.05)
# list of x and y coordinates
x = []
y = []
for t in intervals:
    x.append(u*math.cos(theta)*t)
    y.append(u*math.sin(theta)*t - 0.5*g*t*t)