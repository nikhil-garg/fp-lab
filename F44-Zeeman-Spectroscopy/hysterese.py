import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

I, B1, B2, B3 = np.loadtxt('hysterese.txt', unpack=True, skiprows=1)

B = (B1 + B2 + B3) /3
dB = ((B1*0.02)**2+(B1*0.02)**2+(B1*0.02)**2)**0.5 + (((B1-B)**2+(B2-B)**2+(B3-B)**2)/6)**0.5

Binc = B[:14]
Bdec = B[13:]

dBinc = dB[:14]
dBdec = dB[13:]
dI = 0.2 * np.ones(14)

plt.errorbar(I[:14], Binc, yerr=dBinc, xerr=dI)
plt.errorbar(I[13:], Bdec, yerr=dBdec, xerr=dI)

plt.show()

