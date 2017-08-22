#!/usr/bin/env python

'''
Fortgesschrittenenpraktikum F09/10 - Neuromorphic Computing
Task 3 - A Single Neuron with Synaptic Input

Andreas Gruebl, July 2016, agruebl@kip.uni-heidelberg.de
'''

import numpy as np
import pyNN.hardware.spikey as pynn
import matplotlib.pyplot as plt

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# row and column of synapse
# you can play around with these parameters and the weight to find a "nice" synapse
col = 42
minrow = 42
weight = 10.0

runtime = 400.0
	
pynn.setup(mappingOffset=col)

# list default parameters, for completeness.
# Increase v_thresh in case the neuron fires too early
neuronParams = {
    'v_reset'   : -80.0, # mV 
    'e_rev_I'   : -80.0, # mV
    'v_rest'    : -75.0, # mV
    'v_thresh'  : -55.0, # mV
    'g_leak'    :  20.0  # nS  -> tau_mem = 0.2nF / 20nS = 10ms
}
# the target neuron:
neuron = pynn.Population(1, pynn.IF_facets_hardware1, neuronParams)

# dummy synapse drivers to obtain minrow distance
dummy = pynn.Population(minrow, pynn.SpikeSourceArray)

print pynn.IF_facets_hardware1.default_parameters

synarray = []
# spike times for input stimulus
spiketimes = np.arange(100.0, 151.0, 10.0)
stimarray = [{'spike_times' : [time]} for time in spiketimes]
prjarray = []

# use separate synapses for the consecutive PSPs since a single synapse does not
# linearly stack overlapping PSPs. This only happens at the neuron.
for stim in stimarray:
	synarray.append(pynn.Population(1, pynn.SpikeSourceArray, stim))
	
# connect synapses to target neuron
for syn in synarray:
	prjarray.append(pynn.Projection(syn, neuron,
					method=pynn.AllToAllConnector(weights=weight * pynn.minExcWeight()),
					target='excitatory'))

# in case the synapses are too stron/weak you can either tune their individual
# weights, or the setDrvifallFactors of the according line drivers
for prj in prjarray:
	prj.setDrvifallFactors([.15])


pynn.record_v(neuron[0], '')
neuron.record()

pynn.run(runtime)

spikes = neuron.getSpikes()[:,1]

mem = pynn.membraneOutput

#mem = moving_average(mem, n=20)

membrane = np.array(zip(pynn.timeMembraneOutput, mem))

pynn.end()

# plot
import matplotlib.pyplot as plt

# draw raster plot
ax = plt.subplot(311) #row, col, nr
for spike in spiketimes:
    ax.axvline(x=spike)
ax.set_xlim(0, runtime)
ax.set_ylabel('input spikes')
ax.set_xticklabels([])
ax.set_yticks([])
ax.set_yticklabels([])

ax = plt.subplot(312) #row, col, nr
for spike in spikes:
    ax.axvline(x=spike)
ax.set_xlim(0, runtime)
ax.set_ylabel('spikes')
ax.set_xticklabels([])
ax.set_yticks([])
ax.set_yticklabels([])

# draw membrane potential
axMem = plt.subplot(313)
axMem.plot(membrane[:,0], membrane[:,1])
axMem.set_xlim(0, runtime)
axMem.set_xlabel('time (ms)')
axMem.set_ylabel('membrane potential (mV)')
plt.savefig('resonant_firing.png')
