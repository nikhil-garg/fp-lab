#!/usr/bin/env python

'''
Fortgesschrittenenpraktikum F09/10 - Neuromorphic Computing
Task 5 - Feedforward Networks (Synfire Chain)

Andreas Gruebl, July 2016, agruebl@kip.uni-heidelberg.de

Random network with purely inhibitory connections.
Neurons are driven by setting resting potential over spiking threshold.

See also:
Pfeil et al. (2014).
The effect of heterogeneity on decorrelation mechanisms in spiking neural networks: a neuromorphic-hardware study.
arXiv:1411.7916 [q-bio.NC].
'''

# for plotting without X-server
import matplotlib as mpl
mpl.use('Agg')

import pyNN.hardware.spikey as pynn
import numpy as np

import quantities as q 
import elephant as e
from neo.core import SpikeTrain

import matplotlib.pyplot as plt

pynn.setup()

# set resting potential over spiking threshold
runtime = 1000.0 #ms
popSize = 192

# the following three parameters can be tuned for "optimal decorrelation"
w = 16.0
weight = w * pynn.minInhWeight() #default 4.0
numInhPerNeuron = 25 #default 25
neuronParams = {
    'v_reset'   : -80.0, # mV  # default
    'e_rev_I'   : -80.0, # mV  # default
    'v_rest'    : -35.0, # mV  # for const-current emulation set to > v_thresh #-30.0 default
    'v_thresh'  : -55.0, # mV  # default
    'g_leak'    :  20.0  # nS  -> tau_mem = 0.2nF / 20nS = 10ms
}


neurons = pynn.Population(popSize, pynn.IF_facets_hardware1, neuronParams)

# the inhibitory projection of the complete population to itself, with identical number
# of presynaptic neurons. Enable after measuring the regular-firing case.
pynn.Projection(neurons, neurons, pynn.FixedNumberPreConnector(numInhPerNeuron, weights=weight), target='inhibitory')

# record spikes
neurons.record()

# record membrane potential of first 4 neurons
pynn.record_v([neurons[0], neurons[1], neurons[2], neurons[3]], '')

# start experiment
pynn.run(runtime)

spikes = neurons.getSpikes()

# end experiment (network keeps running...)
pynn.end()

# retrieve spikes and sort neuron-wise. 
snglnrn_spikes = []
snglnrn_spikes_neo = []
for i in range(popSize):
    snglnrn_spikes.append(spikes[np.nonzero(np.equal(i, spikes[:,0])),1][0])
    snglnrn_spikes_neo.append(SpikeTrain(times=snglnrn_spikes[i] * q.ms, t_start=0.0 * q.ms, t_stop=runtime * q.ms))

# generate raster-plot
for i, spiketrain in enumerate(snglnrn_spikes_neo):
        t = spiketrain.rescale(q.ms)
        plt.plot(t, i * np.ones_like(t), 'k.', markersize=2)
plt.axis('tight')
plt.xlim(0, runtime)
plt.xlabel('Time (ms)', fontsize=16)
plt.ylabel('Spike Train Index', fontsize=16)
plt.gca().tick_params(axis='both', which='major', labelsize=14)
plt.savefig('decorr_rasterplot_w{}_k{}.png'.format(w, numInhPerNeuron))

# calculate ISIs and coefficient of variation (CV)
from elephant.statistics import isi, cv
isi_list  = [np.nanmean(isi(spiketrain))       for spiketrain in snglnrn_spikes_neo]
rate_list = [(np.size(spiketrain) / runtime * 1e3) for spiketrain in snglnrn_spikes]
cv_list   = [cv(isi(spiketrain))               for spiketrain in snglnrn_spikes_neo]


# rate against cv
plt.clf()
plt.scatter(cv_list, rate_list)
plt.xlabel('CV', fontsize=16)
plt.ylabel('av rate [Hz]', fontsize=16)
plt.gca().tick_params(axis='both', which='major', labelsize=14)
plt.title('Firing rates vs CV for w={} and k={}'.format(w, numInhPerNeuron))
plt.savefig('6-2decorr_rate_over_cv_w{}_k{}.png'.format(w, numInhPerNeuron))

# plot isi histo:
plt.clf()
plt.hist(np.nan_to_num(isi_list))
plt.xlabel('ISI', fontsize=16)
plt.ylabel('count', fontsize=16)
plt.gca().tick_params(axis='both', which='major', labelsize=14)
plt.savefig('6-2decorr_isi_histo_w{}_k{}.png'.format(w, numInhPerNeuron))

# plot cv histo:
plt.clf()
plt.hist(np.nan_to_num(cv_list))
plt.xlabel('CV', fontsize=16)
plt.ylabel('count', fontsize=16)
plt.gca().tick_params(axis='both', which='major', labelsize=14)
plt.savefig('6-2decorr_cv_histo_w{}_k{}.png'.format(w, numInhPerNeuron))


# to get a feeling for the average activity...:
print 'mean firing rate:', round(len(spikes) / runtime / popSize * 1000.0, 1), '1/s'

print('Mean of av rate:', np.mean(rate_list))
print('std of av rate:', np.std(rate_list))
print('Mean of cv list:', np.nanmean(cv_list))
print('std of cv list:', np.nanstd(cv_list))
#print(cv_list)
