#!/usr/bin/env
# -*- coding: utf-8 -*-

'''
FP Fortgeschrittenenpraktikum Uni Heidelberg
Versuch E01: Elektronik
Fitten an die Frequenzgänge
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Messwerte zur Emitterschaltung einlesen
# Einlesen der Daten aus Tabelle 1
f1, U_E1, dU_E1, U_A1, dU_A1 = np.loadtxt('tab1.txt', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

# Spannungsverstärkung mit Fehler berechnen
V_U1 = U_A1 / U_E1
dV_U1 = V_U1*np.sqrt((dU_A1/U_A1)**2+(dU_E1/U_E1)**2)


# Definition der Ausgleichsgerade y=f(x)
def gerade(x, t):
    return 0*x + t


# Bester Fit an die Geraden 
popt2, pcov2 = curve_fit(gerade, f1[9:-11], V_U1[9:-11]) # Gerade

# Abweichung ist Wurzel aus Diagonalelementen der Kovarianzmatrix
perr1 = np.sqrt(np.diag(pcov1))
perr2 = np.sqrt(np.diag(pcov2))

# Definiere Werte zum Plotten des fits
x = np.linspace(-15.0, 10000000.0, 1000)

print(np.mean(V_U1[19:-13]))
print(np.mean(dV_U1[19:-13]))

# Plot 5 erstellen
# Grenzfrequqenz der Emitterschaltung

#plt.yscale('log')
#plt.xscale('log')
plt.ylim((14,18.5))
plt.xlim((40, 200))


plt.errorbar(f1, V_U1, marker='x', yerr=dV_U1, linestyle='--', label='$Datapoints$')

plt.plot(x, gerade(x, *popt2), linestyle='--', label='$t_{fit}=%.2f \pm%.3f$' %(popt2[0], perr2[0]))

plt.axhline(y=popt2[0]+perr2[0], color='black')
plt.axhline(y=popt2[0]-perr2[0], color='black')

plt.legend(title='Legend', borderpad=1, borderaxespad=1, loc='best', shadow='true')
plt.xlabel(r'Frequenz $f$ in Hz')
plt.ylabel(r'Verstärkung $V_U$')
plt.title(r'Plot 5: Grenzfrequenz Emitterschaltung mit Fit')
plt.savefig('plot05.pdf',format='pdf')
plt.show()



# Messwerte zur Kollektorschaltung einlesen
# Einlesen der Daten aus Tabelle 2
f2, U_E2, dU_E2, U_A2, dU_A2 = np.loadtxt('tab2.txt', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

# Verstärkung der Schaltung berechnen
V_U2 = U_A2 / U_E2
dV_U2 = V_U2*np.sqrt((dU_A2/U_A2)**2+(dU_E2/U_E2)**2)



# Bester Fit an die Geraden 
popt2, pcov2 = curve_fit(gerade, f2[10:], V_U2[10:]) # Gerade 2

# Abweichung ist Wurzel aus Diagonalelementen der Kovarianzmatrix
perr2 = np.sqrt(np.diag(pcov2))

# Definiere Werte zum Plotten des fits
x = np.linspace(-15.0, 10000000.0, 1000)

print(np.mean(V_U1[19:-13]))
print(np.mean(dV_U1[19:-13]))

# Plot 6 erstellen
# Grenzfrequqenz der Kollektorschaltung

#plt.yscale('log')
#plt.xscale('log')
plt.ylim((0.8,1.01))
plt.xlim((50, 300))
plt.errorbar(f2, V_U2, marker='x', yerr=dV_U2, linestyle='--', label='$Datapoints$')

plt.plot(x, gerade(x, *popt2), linestyle='--', label='$t_{fit}=%.2f \pm%.3f$' %(popt2[0], perr2[0]))

plt.axhline(y=popt2[0]+perr2[0], color='black')
plt.axhline(y=popt2[0]-perr2[0], color='black')

plt.legend(title='Legend', borderpad=1, borderaxespad=1, loc='best', shadow='true')
plt.xlabel(r'Frequenz $f$ in Hz')
plt.ylabel(r'Verstärkung $V_U$')
plt.title('Plot 6: Grenzfrequenz Kollektorschaltung mit Fit')
plt.savefig('plot06.pdf',format='pdf')
plt.show()



