import numpy as np

# Werte für Quartz: 
a = 4.91340e-10
b = a
c = 5.40520e-10

lamb = 0.39e-10
k = 2*np.pi/lamb
# k = 16.11073 1/Angström
q = 6.883e10 #1/Angström

# hkl's der Ebenen: 
hkls = [[2, -1, 0], [1, -1, 0], [2, -2, 1], [1, -2, 0], [2, -2, 1]]

print('k:', k*1e-10, '1/A')
print('2pi/a', 2*np.pi/a*1e-10, '1/A')
print('Radius Ewald Sphäre:', k/(2*np.pi/a))
print('Praktisch Ewald Radius:', q/(2*np.pi/a))



quit()

for i in range(5):
    for j in range(5):
        if False: #i==j: 
            continue
        else: 
            winkel = np.cos((hkls[i][0]*hkls[j][0]+hkls[i][1]*hkls[j][1]+0.5*(hkls[i][0]*hkls[j][1]+hkls[i][0]*hkls[j][1]))*(2/(a*np.sqrt(3))**2)+((hkls[i][2]*hkls[j][2])/c**2)/
                              (np.sqrt((hkls[i][0]**2+hkls[i][1]**2+hkls[i][0]*hkls[i][1])*(2/(a*np.sqrt(3)))**2+(hkls[i][2]**2/c**2))*
                               np.sqrt((hkls[j][0]**2+hkls[j][1]**2+hkls[j][0]*hkls[j][1])*(2/(a*np.sqrt(3)))**2+(hkls[j][2]**2/c**2))))
            print('Ebene 1,   Ebene 2,   Winkel')
            print(hkls[i], hkls[j], np.arccos(winkel)*180/np.pi, '°')
            print()