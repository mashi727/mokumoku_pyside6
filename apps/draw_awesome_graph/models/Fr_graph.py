'''
for xy plot

The relationship between gravitational force and distance between two bodies.
'''

name_of_graph = 'Gravitational force and distance'
name_of_xaxis = 'Distance in meters(r))'
name_of_yaxis = 'Gravitational force in newtons(F))'
symbolSize = 10

x = range(100,1001,50)
y = []
G = 6.674*(10**-11)
m1 = 0.5
m2 = 1.5

for dist in x:
    force = G*(m1*m2)/(dist**2)
    y.append(force)