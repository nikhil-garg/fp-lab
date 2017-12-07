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


# Linear Fit
def linear(x,b,c):
    return b + c*x

popt1,pcov1=curve_fit(linear, I[:12], Binc[:-2]) #evtl hier noch sigma, also fehler hinzufügen
popt2,pcov2=curve_fit(linear, I[15:], Bdec[2:])

perr1 = np.sqrt(np.diag(pcov1))
perr2 = np.sqrt(np.diag(pcov2))

print('popt und perr des ersten Fits y = a + 0* x')
print(popt1, perr1)
print('popt und perr des zweiten Fits y = b+c*x')
print(popt2, perr2)

chisq1 = np.sum((linear(I[:12],*popt1)-Binc[:-2])**2/dI[:12]**2)
dof=11 # degrees of freedom
chisq_red1=chisq1/dof
prob1=round(1-chi2.cdf(chisq1,dof),2)*100

chisq2 = np.sum((linear(I[15:],*popt2)-Bdec[2:])**2/(np.ones(12)*0.2)**2)
chisq_red2=chisq2/dof
prob2=round(1-chi2.cdf(chisq2,dof),2)*100

print('chisq_red1=',chisq_red1)
print('chisq_red2=',chisq_red2)
print('Fitwahrscheinlichkeit1=',prob1,'%')
print('Fitwahrscheinlichkeit2=',prob2,'%')


x = np.linspace(-3,17, 100)

plt.errorbar(I[:14], Binc, yerr=dBinc, xerr=dI, linestyle='none', label=r'$Zunehmende\ Stromstärke$')
plt.errorbar(I[13:], Bdec, yerr=dBdec, xerr=dI, linestyle='none', label=r'$Abnehmende\ Stromstärke$')

plt.plot(x, linear(x, *popt1), label=r'$Fit_1\ zunehmende\ Werte$')
plt.plot(x, linear(x, *popt2), label=r'$Fit_2\ abnehmende\ Werte$')

plt.rcParams["font.family"]='serif'
plt.legend(title='Messwerte mit Fit $y=m*x+t$', borderpad=0.3, borderaxespad=0.8, 
           loc='upper left', shadow='true', fontsize=10)

plt.title('Messung des Hysterese Effektes')
plt.ylabel(r'$Magnetische\ Feldstärke\ in\ T$')
plt.xlabel(r'$Stromstärke\ in\ A$')
plt.xlim((-1, 14))
plt.ylim((-0.03, 0.7))

plt.text(5, 0.2, u'$ F_1 = (%.3f \pm%.3f)*x + (%.3f \pm%.3f)$' %(popt1[1], perr1[1], popt1[0], perr1[0]), fontsize=10)
plt.text(5, 0.15, u'$ F_2 = (%.3f \pm%.3f)*x + (%.3f \pm%.3f)$' %(popt2[1], perr2[1], popt2[0], perr2[0]), fontsize=10)
plt.text(5, 0.10, u'$\chi_{red1}^{2}=%.5f, \ Fit_1w\'keit=%.1f $' %(chisq_red1, prob1), fontsize=10)
plt.text(5, 0.05, u'$\chi_{red2}^{2}=%.5f, \ Fit_2w\'keit=%.1f $' %(chisq_red2, prob2), fontsize=10)



'''
plt.text(9, 0.40, u'$ F_1 = m_{fit}=%.3f \pm%.3f$' %(popt[0], perr[0]), fontsize=10)
plt.text(-300, 15, u'$\chi^{2}=%.2f$' %(chisquare), fontsize=10)
plt.text(-300, 12, u'$\chi_{red}^{2}=%.2f $' %(chisquare_red), fontsize=10)
plt.text(-300, 9, u'$P=%.2f $' %(prob) + '%', fontsize=10)
'''

#plt.savefig('hysterese-neu.pdf')
plt.show()

