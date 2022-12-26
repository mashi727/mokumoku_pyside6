'''
for xy plot

Lissajous Curve
'''

name_of_graph = 'Lissajous Curve'
name_of_xaxis = 'ｘ'
name_of_yaxis = 'y'
symbolSize = 7

import numpy as np

m = 4
n = 6
t = np.linspace(-np.pi,np.pi,200)
x = np.sin(m * t)
y = np.sin(n * t)