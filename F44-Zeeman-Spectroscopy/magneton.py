import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2
import numpy.polynomial.polynomial as poly
%matplotlib inline



dk = np.array([0.18554886335208626, -0.17235662237320304, 
      0.22956107403154619, -0.21790912424954087, 
      0.26616910733713511, -0.24974398647888987])

ddk= np.array([0.0055302127107540455, 0.0067252556838207061, 
      0.006469041829205744, 0.0064829686322140784, 
      0.0089495289848316312, 0.0072970083488011839])

#Bfeld = np.array([0.440,0.440, 0.528, 0.528, 0.592 , 0.592])
Bfeld = np.array([0.463, 0.463, 0.559, 0.559, 0.629, 0.629])
dBfeld= np.array([0.009, 0.009, 0.007, 0.007, 0.004, 0.004])

lamCd = 643.80e-9 #bisher noch Literaturwert, nicht eigene Messung
dlamCd = 0.06e-9 # Fehler könnte so groß sein

h = 6.626070040e-34 #J*s
c = 299792458 #m/s

n = 1.4567
d = 0.00404

Deltalam = (lamCd**2 / (2*d*np.sqrt(n**2 - 1)))*np.ones(len(dk))
dDeltalam = 2*(dlamCd/lamCd)*np.ones(len(dk))*Deltalam

delLam = np.abs(dk) * Deltalam
ddelLam = np.sqrt((np.abs(ddk)*Deltalam)**2 + (dDeltalam*ddk)**2)

deltaE = (h*c)/lamCd - (h*c)/(lamCd + delLam)
ddeltaE = h*c*ddelLam/((lamCd + delLam)**2) 

ddeltaE2 = np.sqrt(((h*c*ddelLam)/(lamCd+delLam)**2)**2+
                  (((-h*c/lamCd**2+(h*c)/((lamCd+delLam)**2))*dlamCd)**2))

muB = deltaE/Bfeld
dmuB = np.sqrt((ddeltaE/Bfeld)**2 + (dBfeld*(deltaE/Bfeld**2))**2)




def fddeltaE(lamCd, delLam, dlamCd, ddelLam):
    return np.sqrt((ddelLam*h*c/(lamCd+delLam)**2)**2 +
                   (dlamCd*((h*-1*c/(lamCd**2)) + h*c/(lamCd+delLam)**2))**2)

ddeltaE2 = fddeltaE(lamCd, delLam, dlamCd, ddelLam)




# Plotte delta E gegen B, letzte Aufgabe von Teil 1

# Linear Fit
def linear(x,b,c):
    return b + c*x

popt1,pcov1=curve_fit(linear, Bfeld, deltaE, sigma=ddeltaE)
perr1 = np.sqrt(np.diag(pcov1))
print('popt und perr des ersten Fits y = a + b* x')
print(popt1, perr1)


chisq1 = np.sum((linear(Bfeld, *popt1)-deltaE)**2/ddeltaE**2)
dof=4 # degrees of freedom
chisq_red1=chisq1/dof
prob1=round(1-chi2.cdf(chisq1,dof),2)*100
print(chisq_red1)
print(prob1)

xachse = np.linspace(0.4, 0.65, 1000)
plt.plot(xachse, linear(xachse, *popt1), label='Fitgerade')

plt.text(0.52, 4.1e-24, u'$\chi_{red}^{2}=%.6f$ \n$Fitw\'keit=%.1f $' %(chisq_red1, prob1), fontsize=10)
#plt.text(1,4, 'hallo')


plt.errorbar(Bfeld[::2], deltaE[::2], xerr=dBfeld[::2], yerr=ddeltaE[::2], linestyle='none', marker='2', markersize='14', mew='1.2', label='$\sigma^+$-Linien')
plt.errorbar(Bfeld[1::2], deltaE[1::2], xerr=dBfeld[1::2], yerr=ddeltaE[1::2], linestyle='none', marker='1', markersize='14', mew='1.2', label='$\sigma^-$-Linien')

plt.xlabel('Magnetfeld $B\ [T]$')
plt.ylabel('Energieshift $\Delta E \ [J/T]$')

plt.ylim((3.0e-24, 6.5e-24))

plt.text(0.52, 3.38e-24, u'$Fit: y = m*x + t$ \n$m = (%.2f \pm %.2f) \cdot 10^{-24}$ \n$t = -(%.2f \pm %.2f) \cdot 10^{-25}$' %(popt1[1]*1e24, perr1[1]*1e24, popt1[0]*-1e25, perr1[0]*1e25), fontsize=10)




plt.title('Bohrsches Magneton aus linearem Fit')
plt.legend(title='Legende', borderpad=0.7, borderaxespad=1.0, 
           loc='upper left', shadow='true', fontsize=10)
plt.savefig('methode2.pdf')
plt.show()