'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuum 

Plot: Saugleistung der TMP = druckangepasstes Saugvermögen * Druck
'''

import numpy as np
import matplotlib.pyplot as plt

def S(V, t):
    return V/t

def dS(V, dV, t, dt):
    return np.sqrt(((1/t)*dV)**2 + ((V/t**2)*dt)**2)

# Einlesen der ersten Messwerte
p, dp, t, dt, V, dV = np.loadtxt('tab1.txt', unpack=True, skiprows=1)

V = V * 0.001 #von MilliLiter nach Liter umrechnen
dV = dV * 0.001
p = p *0.001
dp = dp *0.001
p_atmos = 1.01325 #mbar

S_p = np.array(list(S(V, t)[:6]*(p_atmos/p[:6])) + list(S(V, t)[6:]*(p_atmos/p[6:])))
dS_p = np.array(list(np.sqrt((dS(V, dV, t, dt)[:6]/p[:6])**2+(dp[:6]*S(V, t)[:6]/(p[:6])**2)**2)) + list(np.sqrt((dS(V, dV, t, dt)[6:]/p[6:])**2+(dp[6:]*S(V, t)[6:]/(p[6:])**2)**2)))

# Plot erstellen
plt.errorbar(p[:6], (S_p*p)[:6], xerr=dp[:6], yerr=(dS_p*p)[:6], markersize='10', mew=1.2, fmt='x', label='Kapillare')
plt.errorbar(p[6:], (S_p*p)[6:], xerr=dp[6:], yerr=(dS_p*p)[6:], markersize='10', fmt='x', mew=1.2, label='Kolbenprober')

plt.title('Diagramm 6: Saugleistung Q der Turbomolekularpumpe (TMP)')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)
plt.xscale('log')
plt.yscale('log')
plt.xlim(7e-9, 2e-3)
plt.xlabel(r'Druck $p\ [bar]$')
plt.ylabel(r'Saugleistung $Q = S \cdot p_a \ [\frac{l}{s} \cdot bar] $')
plt.savefig('Diagramm06.pdf')
plt.show()

