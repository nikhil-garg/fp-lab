'''
Mechanics and Vacuum

Fortgeschrittenen Praktikum Uni Heidelberg
F70: Mechanik und Vakuum 

Theoretische Berechnung der Leitwerte
'''

from sympy import *
import numpy as np
init_printing(use_latex='mathjax')
from sympy.physics import units as u

r_r = 1.66/2 * u.cm
dr_r = 0.01 * u.cm
#pbar = dp_r[3] * u.milli * u.bar * 1/2 #Druckdifferenz in Bereich der für die Bestimmung der Leitwerte verwendet wurde
pbar = 1.0e-4 * u.milli * u.bar * 1/2
eta = 17.1*u.micro*u.pascal*u.second #Viskosität Luft https://de.wikipedia.org/wiki/Viskosität
l = u.meter #länge Rohr GESCHÄTZT
dl = 0.5 * u.meter #länge Rohr GESCHÄTZT
L_r_theo = (np.pi/8) * r_r**4 * (pbar/(l*eta))

print('L_r_theo:', L_r_theo)

dL_r_theo = L_r_theo * sqrt( (dl/l)**2 + (dr_r/r_r)**2 )
print('dL_r_theo:', dL_r_theo)


r_b = 0.41 * u.cm
dr_b = 0.05 * u.cm
L_b_theo = 362 * r_b**2 * (u.meter/u.second)
print('L_b_theo:', L_b_theo)

dL_b_theo = 362 * dr_b**2 * (u.meter/u.second)
print('dL_b_theo:', dL_b_theo)


#Parrallel
L_rb_1 = ( (1/L_r_theo) +  (1/L_b_theo) )**(-1)
print('L_rb_1:', L_rb_1)


x = (( (1/L_r_theo) + (1/L_b_theo) )**(-2) * L_r_theo**(-2) * dL_r_theo)**2
y = (( (1/L_r_theo) + (1/L_b_theo) )**(-2) * L_b_theo**(-2) * dL_b_theo)**2
dL_rb_1 = ( x + y )**(1/2)
print('dL_rb_1:', dL_rb_1)


#Reihe
L_rb_2 = L_r_theo + L_b_theo
print('L_rb_2:', L_rb_2)

print(L_rb_mess, L_r_mess, L_b_mess)
print(dL_rb_mess, dL_r_mess, dL_b_mess)

print(L_rb_1, L_r_theo, L_b_theo)
print(dL_rb_1, dL_r_theo, dL_b_theo)

print(L_rb_mess, L_rb_1)
print(L_r_mess, L_r_theo)
print(L_b_mess, L_b_theo)

L_rb_1 = L_rb_1 *u.s/u.m**3
L_r_theo = L_r_theo *u.s/u.m**3
L_b_theo = L_b_theo *u.s/u.m**3
dL_rb_1 = dL_rb_1 *u.s/u.m**3
dL_r_theo = dL_r_theo *u.s/u.m**3
dL_b_theo = dL_b_theo *u.s/u.m**3

#Abweichung in %
print(((L_rb_mess-L_rb_1)*100)/L_rb_mess)
print(((L_r_mess-L_r_theo)*100)/L_r_mess)
print(((L_b_mess-L_b_theo)*100)/L_b_mess)

#Abweichung in Standartabweichungen
print((L_rb_mess-L_rb_1)/dL_rb_1)
print((L_r_mess-L_r_theo)/dL_r_theo)
print((L_b_mess-L_b_theo)/dL_b_theo)

#Abweichung in Standartabweichungen
print((L_rb_mess-L_rb_1)/dL_rb_mess)
print((L_r_mess-L_r_theo)/dL_r_mess)
print((L_b_mess-L_b_theo)/dL_b_mess)
