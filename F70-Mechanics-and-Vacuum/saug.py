'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuum 
Teil 1: Auswertung Tabelle 1, Saugvermögen der TMP

Plot: Saugvermögen als Funktion des Logarithmus des Drucks auftragen
'''


import numpy as np
import matplotlib.pyplot as plt

def S(V, t):
    return V/t

def dS(V, dV, t, dt):
    return np.sqrt(((1/t)*dV)**2 + ((V/t**2)*dt)**2)


p, dp, t, dt, V, dV = np.loadtxt('tab1.txt', unpack=True, skiprows=1)
plt.errorbar(p, S(V, t), xerr=dp, yerr=dS(V, dV, t, dt), markersize='10', fmt='x', linestyle='-')
plt.title('Plot1: Saugvermögen als Funktion des Logarithmus des Drucks')
plt.xscale('log')
plt.xlim(7e-6, 2)
#plt.yscale('log')
plt.xlabel('Druck (logarithmisch)')
plt.ylabel(r'Saugvermögen $S = \frac{dV}{dt}$')
plt.savefig('plot1.pdf')
plt.show()
