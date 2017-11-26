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