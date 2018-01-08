'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuum 
Teil 2.5: Auswertung Tabelle 2 und 3, Leitwerte von Rohr und Blende

Plot: Saugleistung vs Druckdifferenz, Steigung ist Leitwert
'''

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
from scipy.stats import chi2

def dp(p):
    return 0.1 * p

def ddelta_p(p1, p2):
    return np.sqrt(dp(p1)**2 + dp(p2)**2)  

# fitfunktion Fit
def fitfunktion(x,a,b):
    #return a + b*x  
    return a * np.power(x, b)

S = np.array([8.52878465e-07, 5.97014925e-06, 1.64609053e-05, 5.50458716e-05, 1.73010381e-04, 5.10204082e-04, 1.26742712e-03, 2.42718447e-03, 2.60416667e-03, 5.31914894e-03, 8.77192982e-03])
dS = np.array([8.59829473e-08, 4.00707811e-07, 1.09627588e-06, 3.54230302e-06, 1.86945166e-05, 2.99116669e-05, 5.76746798e-05, 9.34316435e-05, 1.06806679e-04, 5.72769256e-04, 2.31879585e-03])


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

# Zu plottende Werte

x2 = o2-u2
x3 = o3-u3
x4 = o4-u4

y2 = S*u2
y3 = S*u3
y4 = S*u4

dx2 = ddelta_p(u2, o2)
dx3 = ddelta_p(u3, o3)
dx4 = ddelta_p(u4, o4)

dy2 = np.sqrt((dS*u2)**2 + (dp(u2)*S)**2)
dy3 = np.sqrt((dS*u3)**2 + (dp(u3)*S)**2)
dy4 = np.sqrt((dS*u4)**2 + (dp(u4)*S)**2)

plt.errorbar(x2, y2, xerr=dx2, yerr=dy2, markersize='10', fmt='x', mew=1.1, label='Nur Rohr', color='b')
plt.errorbar(x3, y3, xerr=dx3, yerr=dy3, markersize='10', fmt='x', mew=1.1, label='Nur Blende', color='g')
plt.errorbar(x4, y4, xerr=dx4, yerr=dy4, markersize='10', fmt='x', mew=1.1, label='Rohr und Blende', color='r')

#Theorie Rohr

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

plt.plot(x2, (Lmol(x2))*x2, label='Theorie molekular')
plt.plot(x2, (Llam(x2))*x2, label='Theorie laminar')


'''
# Fits generieren
x2 = np.log10(x2)
x3 = np.log10(x3)
x4 = np.log10(x4)

y2 = np.log10(y2)
y3 = np.log10(y3)
y4 = np.log10(y4)

dx2 = np.log10(dx2)
dx3 = np.log10(dx3)
dx4 = np.log10(dx4)

dy2 = np.log10(dy2)
dy3 = np.log10(dy3)
dy4 = np.log10(dy4)
'''

#popt21,pcov21=curve_fit(fitfunktion, x2[:6], y2[:6])
#popt22,pcov22=curve_fit(fitfunktion, x2[6:], y2[6:])
#perr21 = np.sqrt(np.diag(pcov21))
#perr22 = np.sqrt(np.diag(pcov22))
#
#popt31,pcov31=curve_fit(fitfunktion, x3[:7], y3[:7])
#popt32,pcov32=curve_fit(fitfunktion, x3[7:], y3[7:])
#perr31 = np.sqrt(np.diag(pcov31))
#perr32 = np.sqrt(np.diag(pcov32))
#
#popt41,pcov41=curve_fit(fitfunktion, x2[:7], y2[:7])
#popt42,pcov42=curve_fit(fitfunktion, x2[7:], y2[7:])
#perr41 = np.sqrt(np.diag(pcov41))
#perr42 = np.sqrt(np.diag(pcov42))
#
##x = np.log10(np.linspace(1e-8, 1e-2, 1000))
#x = np.linspace(1e-8, 1e-2, 1000)
##x = np.logspace(-8, -2, base=10)



#plt.plot(x, fitfunktion(x, *popt21), color='b')
#plt.plot(x, fitfunktion(x, *popt22), color='b')
#
#plt.plot(x, fitfunktion(x, *popt31), color='g')
#plt.plot(x, fitfunktion(x, *popt32), color='g')
#
#plt.plot(x, fitfunktion(x, *popt41), color='r')
#plt.plot(x, fitfunktion(x, *popt42), color='r')

plt.title('Plot 2c: Leitwerte aus Steigung')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)

plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Druckdifferenz $\Delta p = p_{oben}-p_{unten}\ [bar]$')
plt.ylabel(r'Saugleistung $Q = S \cdot p_{unten}$')
plt.savefig('plot2c2.pdf')
plt.show()
