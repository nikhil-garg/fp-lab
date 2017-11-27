''' Zeeman Hysterese Effect'''

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

# Increasing Current
I1 = np.array([6.0, 8.0, 10.0, 12.0])
B1 = np.array([0.327, 0.429, 0.527, 0.592])

# Decreasing Current
I2 = np.array([12.0, 10.0, 8.0, 6.0])
B2 = np.array([0.592, 0.528, 0.440, 0.324])

dI= 0.1
dB=0.003

# Linear Fit
def linear(x,b,c):
    return b + c*x

popt1,pcov1=curve_fit(linear, I1[:-1], B1[:-1]) #evtl hier noch sigma, also fehler hinzufügen
popt2,pcov2=curve_fit(linear, I2[1:], B2[1:])

perr1 = np.sqrt(np.diag(pcov1))
perr2 = np.sqrt(np.diag(pcov2))

print('popt und perr des ersten Fits y = a + 0* x')
print(popt1, perr1)
print('popt und perr des zweiten Fits y = b+c*x')
print(popt2, perr2)