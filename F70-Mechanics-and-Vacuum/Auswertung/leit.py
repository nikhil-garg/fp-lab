'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuum 
Teil 2.5: Auswertung Tabelle 2 und 3, Leitwerte von Rohr und Blende

Plot: Saugvermögen als Funktion des Logarithmus des Drucks auftragen
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

# alte Saugleistungswerte
#S = np.array([8.52878465e-07, 5.97014925e-06, 1.64609053e-05, 5.50458716e-05, 1.73010381e-04, 5.10204082e-04, 1.26742712e-03, 2.42718447e-03, 2.60416667e-03, 5.31914894e-03, 8.77192982e-03])
#dS = np.array([8.59829473e-08, 4.00707811e-07, 1.09627588e-06, 3.54230302e-06, 1.86945166e-05, 2.99116669e-05, 5.76746798e-05, 9.34316435e-05, 1.06806679e-04, 5.72769256e-04, 2.31879585e-03])

# Saugleistung aus Diagramm 04 in bar * liter/sekunde
S = np.array([86.41791045,  183.31071913,  166.79012346,   174.29759174, 175.30276817,   161.55133929,  128.42205323,   72.33366648, 23.98792614, 16.33220503, 8.88815789])
dS = np.array([ 12.11077371,  13.32287762, 19.77734776,   12.30589208, 25.47176612,  10.59239042,  13.92482812,   3.45831415, 2.36109378, 1.8030829, 2.47916957])


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


# Werte der verschiedenen Strömungsbereiche mitteln und ausgeben 
# Laminarströmung, Molekurlarströmung, siehe Protokoll

print()
print('Rohr: Werte 1-3 gemittelt: ')
print(np.mean(L(S, u2, o2-u2)[0:3]), '+-', np.mean((dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2)))[0:3]), 'std', np.std((dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2)))[0:3]))
print()
print('Rohr letzter Wert:')
print((L(S, u2, o2-u2)[-1]), '+-', dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2))[-1])
print()
print('Blende: 1-7 gemittelt:')
print(np.mean(L(S, u3, o3-u3)[0:7]), '+-', np.mean(dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2))[0:7]), 'std', np.std(dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2))[0:7]))
print()
print('Rohr und Blende: Werte 1-4 gemittelt:')
print(np.mean(L(S, u4, o4-u4)[0:4]), '+-', np.mean(dL(S, dS, u4, dp(u4), o4-u4, ddelta_p(o4, u4))[0:4]), 'std', np.std(dL(S, dS, u4, dp(u4), o4-u4, ddelta_p(o4, u4))[0:4]))
print()
print('Rohr und Blende letzter Wert:')
print(L(S, u4, o4-u4)[-1], '+-', dL(S, dS, u4, dp(u4), o4-u4, ddelta_p(o4, u4))[-1])

plt.errorbar(u2, L(S, u2, o2-u2), xerr=dp(u2), yerr=dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2)), markersize='10', fmt='x', mew=1.1, label='Nur Rohr')
plt.errorbar(u3, L(S, u3, o3-u3), xerr=dp(u3), yerr=dL(S, dS, u3, dp(u3), o3-u3, ddelta_p(o3, u3)), markersize='10', fmt='x', mew=1.1, label='Nur Blende')
plt.errorbar(u4, L(S, u4, o4-u4), xerr=dp(u4), yerr=dL(S, dS, u4, dp(u4), o4-u4, ddelta_p(o4, u4)), markersize='10', fmt='x', mew=1.1, label='Rohr und Blende')
# Berechnung:
plt.errorbar(u2, ((L(S, u2, o2-u2))**(-1) + (L(S, u3, o3-u3))**(-1))**(-1), markersize='10', fmt='x', mew=1.1, label='Rohr und Blende Rechnung')


plt.title('Diagramm 8: Leitwerte mit Rohr und Blende')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)
plt.xscale('log')
plt.yscale('log')
#plt.xlim(7e-6, 2)
plt.xlabel(r'Druck unteres Rohrende $p_u\ [bar]$')
plt.ylabel(r'Leitwert $L = \frac{S \cdot p_u}{\Delta{p}}$')
#plt.savefig('Diagramm08.pdf')
plt.show()


plt.errorbar(o2-u2, L(S, u2, o2-u2), xerr=dp(u2), yerr=dL(S, dS, u2, dp(u2), o2-u2, ddelta_p(o2, u2)), markersize='10', fmt='x', mew=1.1, label='Nur Rohr')
plt.errorbar(o3-u3, L(S, u3, o3-u3), xerr=dp(u3), yerr=dL(S, dS, u3, dp(u3), o3-u3, ddelta_p(o3, u3)), markersize='10', fmt='x', mew=1.1, label='Nur Blende')
plt.errorbar(o4-u4, L(S, u4, o4-u4), xerr=dp(u4), yerr=dL(S, dS, u4, dp(u4), o4-u4, ddelta_p(o4, u4)), markersize='10', fmt='x', mew=1.1, label='Rohr und Blende')


plt.errorbar(o2-u2, ((L(S, u2, o2-u2))**(-1) + (L(S, u3, o3-u3))**(-1))**(-1), markersize='10', fmt='x', mew=1.1, label='Rohr und Blende Rechnung')

plt.title('Diagramm 9: Leitwerte mit Rohr und Blende')
plt.legend(title='Messwerte', borderpad=1, borderaxespad=1, loc='best', shadow='true', fontsize=12)

plt.xscale('log')
plt.yscale('log')
#plt.xlim(7e-6, 2)
plt.xlabel(r'Druckdifferenz $p_o-p_u\ [bar]$')
plt.ylabel(r'Leitwert $L = \frac{S \cdot p_u}{\Delta{p}}$')
plt.savefig('Diagramm09.pdf')
plt.show()

