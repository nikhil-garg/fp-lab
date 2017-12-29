'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuum 
Teil 2.5: Auswertung Tabelle 2 und 3, Leitwerte von Rohr und Blende

Plot: Saugleistung vs Druckdifferenz, Steigung ist Leitwert des Rohres
'''

import numpy as np
import matplotlib.pyplot as plt
import math

def S(V, t):
    return V/t

def dS(V, dV, t, dt):
    return np.sqrt(((1/t)*dV)**2 + ((V/t**2)*dt)**2)

def L(S, p_a, delta_p):
    return (S*p_a)/delta_p

def dL(S, dS, p_a, dp_a, delta_p, ddelta_p):
    return L(S, p_a, delta_p) * np.sqrt((dS/S)**2 + (dp_a/p_a)**2 + (ddelta_p/delta_p)**2)

def dp(p):
    return 0.1 * p

def ddelta_p(p1, p2):
    return np.sqrt(dp(p1)**2 + dp(p2)**2)    

#Rohr Daten: 
r = 0.00575 # Radius in m
dr = 0.00010
eta = 17.1e-11 # Viskosität Luft in bar*s
l = 1.0 # Länge in m
dl = 0.002

def Llam(dp):
    return np.pi * r**4 * dp * eta * l / (8*2)

R = 8.31 # Joule/(mol*Kelvin)
T = 293 # Kelvin
M = 14.0067 # Molekulargewicht von Stickstoff in u
u = 1.66e-27 # Gewicht von 1 u in kg

def Lmol(dp):
    return (8/3)*(r**3/l) * np.sqrt((np.pi*R*T)/(2*M)) + 0*dp

S = np.array([8.52878465e-07, 5.97014925e-06, 1.64609053e-05, 5.50458716e-05, 1.73010381e-04, 5.10204082e-04, 1.26742712e-03, 2.42718447e-03, 2.60416667e-03, 5.31914894e-03, 8.77192982e-03])
dS = np.array([8.59829473e-08, 4.00707811e-07, 1.09627588e-06, 3.54230302e-06, 1.86945166e-05, 2.99116669e-05, 5.76746798e-05, 9.34316435e-05, 1.06806679e-04, 5.72769256e-04, 2.31879585e-03])

#S = 80
#dS = 5

u2, o2 = np.loadtxt('tab2.txt', unpack=True, skiprows=1)
u3, o3 = np.loadtxt('tab3.txt', unpack=True, skiprows=1)
u4, o4 = np.loadtxt('tab4.txt', unpack=True, skiprows=1)

#Größenordnung anpassen:
u2 = u2 * 0.001
u3 = u3 * 0.001
u4 = u4 * 0.001
o2 = o2 * 0.001
o3 = o3 * 0.001
o4 = o4 * 0.001


plt.errorbar(o2-u2, L(S, u2, o2-u2), xerr=dp(u2), yerr=dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2)), markersize='10', fmt='x', mew=1.1, label='Nur Rohr')
plt.plot(o2-u2, Llam(o2-u2), label='Theorie laminar')
plt.plot(o2-u2, Lmol(o2-u2), label='Theorie molekular')

#plt.errorbar(o3-u3, L(S, u3, o3-u3), xerr=dp(u3), yerr=dL(S, dS, u3, dp(u3), o3-u3, ddelta_p(o3, u3)), markersize='10', fmt='x', mew=1.1, label='Nur Blende')
#plt.errorbar(o4-u4, L(S, u4, o4-u4), xerr=dp(u4), yerr=dL(S, dS, u4, dp(u4), o4-u4, ddelta_p(o4, u4)), markersize='10', fmt='x', mew=1.1, label='Rohr und Blende')

plt.title('Plot 2b: Leitwerte mit Rohr und Blende')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)

plt.xscale('log')
plt.yscale('log')
#plt.xlim(7e-6, 2)
plt.xlabel(r'Druckdifferenz $p_o-p_u\ [bar]$')
plt.ylabel(r'Leitwert $L = \frac{S \cdot p_u}{\Delta{p}}$')
plt.savefig('plot2b.pdf')
plt.show()