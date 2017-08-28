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


def plotten(x, y, xerror=None, yerror=None, 
            xlim=None, ylim=None, 
            xscale=None, yscale=None,
            xlabel='x-axis', ylabel='y-axis', 
            title=r'Plot-Title', 
            save=False, name='plot.pdf', show=True):
  plt.errorbar(x, y, marker='x', xerr= xerror, yerr=yerror, linestyle='--')
  if xscale:
    plt.xscale(xscale)
  if yscale:
    plt.yscale(yscale)
  if xlim:
    plt.xlim(xlim)
  if ylim:
    plt.ylim(ylim)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  if save:
    plt.savefig(name)
  if show:
    plt.show()

# Messwerte zur Emitterschaltung einlesen
# Einlesen der Daten aus Tabelle 1
f1, U_E1, dU_E1, U_A1, dU_A1 = np.loadtxt('tab1.txt', skiprows=1, usecols=(0,1,2,3,4), unpack=True)

# Spannungsverstärkung mit Fehler berechnen
V_U1 = U_A1 / U_E1
dV_U1 = V_U1*np.sqrt((dU_A1/U_A1)**2+(dU_E1/U_E1)**2)


# Plot 1 erstellen
# Grenzfrequqenz der Emitterschaltung

plotten(f1, V_U1, yerror=dV_U1, xlim=(-10,200), ylim=(5,20), yscale='log', 
  xlabel=r'Frequenz $f$ in Hz', ylabel=r'Verstärkung $V_U$', 
  title=r'Plot 1: Grenzfrequenz Emitterschaltung',
  name='plot01.pdf', save=False)


# Plot 2 erstellen
# Frequenzgang der Emitterschaltung

plotten(f1, V_U1, yerror=dV_U1, xlim=(10, 1800000), ylim=(5,20), 
  xscale='log', yscale='log', 
  xlabel=r'Frequenz $f$ in Hz', ylabel=r'Verstärkung $V_U$', 
  title=r'Plot 2: Frequenzgang Emitterschaltung',
  name='plot02.pdf', save=False)


# Werte in Ausgabedatei schreiben:
# Verstärkungen für Protokoll
'''
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

plotten(f2, V_U2, yerror=dV_U2, xlim=(-2, 230), ylim=(0.2,1.1), yscale='log', 
  xlabel=r'Frequenz $f$ in Hz', ylabel=r'Verstärkung $V_U$', 
  title=r'Plot 3: Grenzfrequenz Kollektorschaltung',
  name='plot03.pdf', save=False)


# Plot 4 erstellen
# Frequenzgang der Kollektorschaltung

plotten(f2, V_U2, yerror=dV_U2, xlim=(8, 1000000), ylim=(0.2,1.1), 
  xscale='log', yscale='log', 
  xlabel=r'Frequenz $f$ in Hz', ylabel=r'Verstärkung $V_U$', 
  title=r'Plot 4: Frequenzgang Kollektorschaltung',
  name='plot04.pdf', save=False)


# Werte in Ausgabedatei schreiben:

'''
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

