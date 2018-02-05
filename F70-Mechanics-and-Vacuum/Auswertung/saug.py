'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuum 
Teil 2.4: Auswertung Tabelle 1, Saugvermögen der TMP

Plot: Saugvermögen als Funktion des Logarithmus des Drucks auftragen
'''

import numpy as np
import matplotlib.pyplot as plt

def S(V, t):
    return V/t

def dS(V, dV, t, dt):
    return np.sqrt(((1/t)*dV)**2 + ((V/t**2)*dt)**2)

# Einlesen der Werte
p, dp, t, dt, V, dV = np.loadtxt('tab1.txt', unpack=True, skiprows=1)

V = V * 0.001 #von MilliLiter nach Liter umrechnen
dV = dV * 0.001
p = p *0.001
dp = dp *0.001
p_atmos = 1.01325 #mbar

#print('p:', p)
#print('dp:', dp)
#print('S:', S(V, t))
#print('dS:', dS(V, dV, t, dt))

print(S(V, t)[:6]*(p_atmos/p[:6]))
print(np.sqrt((dS(V, dV, t, dt)[:6]/p[:6])**2+(dp[:6]*S(V, t)[:6]/(p[:6])**2)**2))

# Plot Saugvermögen
plt.errorbar(p[:6], S(V, t)[:6], xerr=dp[:6], yerr=dS(V, dV, t, dt)[:6], markersize='10', mew=1.2, fmt='x', label='Kapillare')
plt.errorbar(p[6:], S(V, t)[6:], xerr=dp[6:], yerr=dS(V, dV, t, dt)[6:], markersize='10', fmt='x', mew=1.2, label='Kolbenprober')
plt.title('Diagramm 2: Saugvermögen S der Turbomolekularpumpe (TMP)')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)
plt.xscale('log')
plt.yscale('log')
plt.xlim(7e-9, 2e-3)
plt.xlabel(r'Druck $p\ [bar]$')
plt.ylabel(r'Saugvermögen $S = \frac{dV}{dt}$')
plt.savefig('Diagramm02.pdf')
plt.show()


# Plot Druckangepasstes Saugvermögen
plt.errorbar(p[:6], S(V, t)[:6]*(p_atmos/p[:6]), xerr=dp[:6], yerr=np.sqrt((dS(V, dV, t, dt)[:6]/p[:6])**2+(dp[:6]*S(V, t)[:6]/(p[:6])**2)**2), markersize='10', mew=1.2, fmt='x', label='Kapillare')
plt.errorbar(p[6:], S(V, t)[6:]*(p_atmos/p[6:]), xerr=dp[6:], yerr=np.sqrt((dS(V, dV, t, dt)[6:]/p[6:])**2+(dp[6:]*S(V, t)[6:]/(p[6:])**2)**2), markersize='10', fmt='x', mew=1.2, label='Kolbenprober')
plt.title('Diagramm 3: Saugvermögen S der TMP (druckangepasst, loglog)')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)
plt.xscale('log')
plt.yscale('log')
plt.xlim(7e-9, 2e-3)
plt.xlabel(r'Druck $p\ [bar]$')
plt.ylabel(r'Druckangepasstes Saugvermögen $S_p = \frac{dV}{dt} \frac{p_{atmosph}}{p_{rezipient}}$')
plt.savefig('Diagramm03.pdf')
plt.show()


# Plot Saugvermögen (entspricht Diagramm 02)
plt.errorbar(p[:6], S(V, t)[:6]*(p_atmos/p[:6]), xerr=dp[:6], yerr=np.sqrt((dS(V, dV, t, dt)[:6]/p[:6])**2+(dp[:6]*S(V, t)[:6]/(p[:6])**2)**2), markersize='10', mew=1.2, fmt='x', label='Kapillare')
plt.errorbar(p[6:], S(V, t)[6:]*(p_atmos/p[6:]), xerr=dp[6:], yerr=np.sqrt((dS(V, dV, t, dt)[6:]/p[6:])**2+(dp[6:]*S(V, t)[6:]/(p[6:])**2)**2), markersize='10', fmt='x', mew=1.2, label='Kolbenprober')
plt.title('Diagramm 4: Saugvermögen S der TMP (druckangepasst, log)')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)
plt.xscale('log')
#plt.yscale('log')
plt.xlim(7e-9, 2e-3)
plt.xlabel(r'Druck $p\ [bar]$')
plt.ylabel(r'Druckangepasstes Saugvermögen $S_p = \frac{dV}{dt} \frac{p_{atmosph}}{p_{rezipient}}$')
plt.savefig('Diagramm04.pdf')
plt.show()


#plt.errorbar(p[:6], S(V, t)[:6]*p[:6], xerr=dp[:6], yerr=np.sqrt((dS(V, dV, t, dt)[:6]*p[:6])**2+(dp[:6]*S(V, t)[:6])**2), markersize='10', mew=1.2, fmt='x', label='Kapillare')
#plt.errorbar(p[6:], S(V, t)[6:]*p[6:], xerr=dp[6:], yerr=np.sqrt((dS(V, dV, t, dt)[6:]*p[6:])**2+(dp[6:]*S(V, t)[6:])**2), markersize='10', fmt='x', mew=1.2, label='Kolbenprober')
#plt.title('Plot 1c: Saugleistung Q der Turbomolekularpumpe (TMP)')
#plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)
#plt.xscale('log')
#plt.yscale('log')
#plt.xlim(7e-9, 2e-3)
#plt.xlabel(r'Druck $p\ [bar]$')
#plt.ylabel(r'Saugleistung $Q = S \cdot p_a$')
##plt.savefig('plot1c.pdf')
#plt.show()
