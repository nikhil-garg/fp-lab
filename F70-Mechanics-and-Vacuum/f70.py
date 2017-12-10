'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuuum 
'''

import numpy as np
import matplotlib.pyplot as plt

tabellen = ['tab2.txt', 'tab3.txt', 'tab4.txt']

for tab in tabellen:
    c1, c2 = np.loadtxt(tab, unpack=True, skiprows=1)
    plt.plot(c1, c2)
    plt.title(tab)
    plt.savefig(tab[:-3] + '.pdf')
    plt.show()
