#!/usr/bin/env
# -*- coding: utf-8 -*-

'''
FP Fortgeschrittenenpraktikum Uni Heidelberg
Versuch E01: Elektronik
Auswertung zu Teil 1 und 2

Plotten von Frequenzgang und Grenzfrequenz
von Emitter- und Kollektorschaltung 
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

# Plot 1 erstellen
# Grenzfrequqenz der Emitterschaltung

plt.yscale('log')
plt.ylim((5,20))
plt.xlim((-10, 200))
plt.errorbar(f1, V_U1, marker='x', yerr=dV_U1, linestyle='--')
plt.xlabel(r'Frequenz $f$ in Hz')
plt.ylabel(r'Verstärkung $V_U$')
plt.title(r'Plot 1: Grenzfrequenz Emitterschaltung')
#plt.savefig('plot01.pdf',format='pdf')
plt.show()


# Plot 2 erstellen
# Frequenzgang der Emitterschaltung

plt.yscale('log')
plt.xscale('log')
plt.ylim((5,20))
plt.xlim((10, 1800000))
plt.errorbar(f1, V_U1, marker='x', yerr=dV_U1, linestyle='--')
plt.xlabel('Frequenz $f$ in Hz')
plt.ylabel('Verstärkung $V_U$')
plt.title('Plot 2: Frequenzgang Emitterschaltung')
#plt.savefig('plot02.pdf',format='pdf')
plt.show()

'''
# Werte in Ausgabedatei schreiben:
# Verstärkungen für Protokoll

with open('daten1_achtung_neu_berechnet.txt', 'w') as file:
    file. write('f  U_E dU_E    U_A     dU_A    V_U dV_U\n')
    for i in range(len(f)):
        file.write(str(f1[i])[:-2]+' '+
                   str(U_E1[i])+'    '+
                   str(dU_E1[i])+'   '+
                   str(U_A1[i])+'    '+
                   str(dU_A1[i])+'   '+
                   str(round(V_U1[i],2))+'   '+
                   str(round(dV_U1[i],2))+'\n')
'''


# Messwerte zur Kollektorschaltung einlesen
# Einlesen der Daten aus Tabelle 2
f2, U_E2, dU_E2, U_A2, dU_A2 = np.loadtxt('tab2.txt', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

# Verstärkung der Schaltung berechnen
V_U2 = U_A2 / U_E2
dV_U2 = V_U2*np.sqrt((dU_A2/U_A2)**2+(dU_E2/U_E2)**2)

# Plot 3 erstellen
# Grenzfrequqenz der Kollektorschaltung

plt.yscale('log')
plt.ylim((0.2,1.1))
plt.xlim((-2, 230))
plt.errorbar(f2, V_U2, marker='x', yerr=dV_U2, linestyle='--')
plt.xlabel('Frequenz $f$ in Hz')
plt.ylabel('Verstärkung $V_U$')
plt.title('Plot 3: Grenzfrequenz Kollektorschaltung')
#plt.savefig('plot03.pdf',format='pdf')
plt.show()


# Plot 4 erstellen
# Frequenzgang der Kollektorschaltung

plt.yscale('log')
plt.xscale('log')
plt.ylim((0.2,1.1))
plt.xlim((8, 1000000))
plt.errorbar(f2, V_U2, marker='x', yerr=dV_U2, linestyle='--')
plt.xlabel('Frequenz $f$ in Hz')
plt.ylabel('Verstärkung $V_U$')
plt.title('Plot 4: Frequenzgang Kollektorschaltung')
#plt.savefig('plot04.pdf',format='pdf')
plt.show()


'''
# Werte in Ausgabedatei schreiben:
with open('daten2_achtung_neu_berechnet.txt', 'w') as file:
    file. write('f  U_E dU_E    U_A     dU_A    V_U dV_U\n')
    for i in range(len(f)):
        file.write(str(f2[i])[:-2]+' '+
                   str(U_E2[i])+'    '+
                   str(dU_E2[i])+'   '+
                   str(U_A2[i])+'    '+
                   str(dU_A2[i])+'   '+
                   str(round(V_U2[i],2))+'   '+
                   str(round(dV_U2[i],2))+'\n')

'''                   

