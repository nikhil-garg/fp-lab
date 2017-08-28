import numpy as np
import matplotlib.pyplot as plt

'''
m1 = np.loadtxt('avg_cvs_over_w_and_K.txt').reshape((15,25))

plt.pcolor(m1, cmap=plt.cm.jet)

plt.title("Plot of average CVs over w and K")
plt.xlabel("Number of presynaptic partners K")
plt.ylabel("Inhibitory weight w")
plt.colorbar()
plt.savefig('6-2-average-CVs-over-w-and-k-jet.png')
#plt.show()
plt.clf()


m2 = np.loadtxt('avg_rate_over_w_and_K.txt').reshape((15,25))

plt.pcolor(m2, cmap=plt.cm.jet)
plt.title("Plot of average rates over w and K")
plt.xlabel("Number of presynaptic partners K")
plt.ylabel("Inhibitory weight w")
plt.colorbar()
plt.savefig('6-2-average-rates-over-w-and-k-jet.png')
#plt.show()
plt.clf()


 
data = np.loadtxt('g-leak-params.txt')
print data

plt.title('Histogram of $g_{leak}$-values for Calibration')
plt.xlabel('$g_{leak}-value$')
plt.hist(data, facecolor='blue')
plt.savefig('2-4-histogram-g-leak-values.pdf')
plt.show()

'''

diff_mean1 = np.loadtxt('2-4a-calibrated-histogram.txt')
diff_mean2 = np.loadtxt('2-4a-non-calibrated-histogram.txt')

n, bins, patches = plt.hist(diff_mean2, 20, facecolor='green', alpha=0.7, label=r'Non-Calibrated: $\bar{\tau}=%.2f \pm %.2f$'  %(np.mean(diff_mean2), np.std(diff_mean2)))
n, bins, patches = plt.hist(diff_mean1, 20, facecolor='blue', alpha=0.7, label=r'Calibration target $\tau_m = 15ms$' '\n' r'Calibrated: $\bar{\tau}=%.2f \pm %.2f$'  %(np.mean(diff_mean1), np.std(diff_mean1)))



plt.xlabel(r'$\tau_m[ms]$')
plt.ylabel(r'$Neurons$')
plt.title(r'Distribution of firing rates (192 neurons)')
plt.legend(title='Legend', loc='best', borderaxespad=1, borderpad=1, shadow='true')

plt.grid(True)
plt.savefig('2-4-calibration-histogram.png')
