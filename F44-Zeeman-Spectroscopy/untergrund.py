'''
Skript zur Reduktion des Untergrundes der Messdaten des Zeemann Versuches
'''

import numpy as np
import matplotlib.pyplot as plt
import peakutils
%matplotlib inline

# Importiere Daten zu Transversal mit B Feld
x1, y1 = np.loadtxt('/Users/Oskar/Code/fp-lab/F44-Zeeman-Spectroscopy/data-part1/07-transversal-mit-B-8-A.txt', skiprows=0, usecols=(0,1), unpack=True)


# Plot der Rohdaten
plt.plot(x1, y1)

print(np.min(y1[:2000]))

werte = (y1 + np.ones(len(y1))*(np.abs(np.min(y1[:2000]))))[0:2000]

#plt.plot(x1[0:2000], werte)


baseline_values = peakutils.baseline(werte, 10)
plt.plot(baseline_values)
plt.plot(werte)


plt.plot(baseline_values - np.ones(len(baseline_values))*0.002*1e8)
plt.plot(werte)


plt.plot((werte-(baseline_values - np.ones(len(baseline_values))*0.002*1e8)))


np.savetxt('trans8A.txt', 
           np.transpose([x1[600:2000],
                         (werte-(baseline_values - np.ones(len(baseline_values))*0.005*1e8))[600:]]),
          fmt='%.f %.3f')


# Importiere Daten zu Transversal mit B Feld
x4, y4 = np.loadtxt('/Users/Oskar/Code/fp-lab/F44-Zeeman-Spectroscopy/trans10A.txt', skiprows=0, usecols=(0,1), unpack=True)


plt.plot(data)
baseline = peakutils.baseline(data, tol=-2e7)
plt.plot(baseline)
