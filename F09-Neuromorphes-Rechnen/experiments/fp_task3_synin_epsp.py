#!/usr/bin/env python

'''
Fortgesschrittenenpraktikum F09/10 - Neuromorphic Computing
Task 3 - A Single Neuron with Synaptic Input

Andreas Grübl, July 2016, agruebl@kip.uni-heidelberg.de
'''


import pyNN.hardware.spikey as pynn
import numpy as np
import matplotlib.pyplot as plt

weight             = 15.0        # synaptic weight in digital values
runtime            = 1000 * 1000.0 # runtime in biological time domain in ms
durationInterval   = 200.0       # interval between input spikes in ms
neuronIndex        = 42          # choose neuron on chip in range(384)
synapseDriverIndex = 42          # choose synapse driver in range(256)

pynn.setup(mappingOffset=neuronIndex, calibSynDrivers=False) #turn off calibration of synapse line drivers

##build network
neurons = pynn.Population(1, pynn.IF_facets_hardware1)
pynn.record_v(neurons[0], '')

#allocate dummy synapse drivers sending no spikes
if synapseDriverIndex > 0:
    stimuliDummy = pynn.Population(synapseDriverIndex, pynn.SpikeSourceArray, {'spike_times': []})
    prj = pynn.Projection(stimuliDummy, neurons, pynn.AllToAllConnector(weights=0), target='inhibitory')

#allocate synapse driver and configure spike times
stimProp = {'spike_times': np.arange(durationInterval, runtime - durationInterval, durationInterval)}
stimuli = pynn.Population(1, pynn.SpikeSourceArray, stimProp)
prj = pynn.Projection(stimuli, neurons, pynn.AllToAllConnector(weights=weight * pynn.minInhWeight()), target='inhibitory')

# modify properties of synapse driver
# drvifall controls the slope of the falling edge of the PSP shape.
# smaller values increase the length, thus the total charge transmitted by the synapse, thus the PSP height.
print 'Range of calibration factors of drvifall for excitatory connections', prj.getDrvifallFactorsRange('inh')
prj.setDrvifallFactors([0.2])
#prj.setDrvioutFactors([1.0])

##run network
pynn.run(runtime)
mem = pynn.membraneOutput
time = pynn.timeMembraneOutput
pynn.end()

######
##calculate spike-triggered average of membrane potential
timeNorm = time - time[0]
#number of data points per interval
lenInterval = np.argmin(abs(time - durationInterval))
#number of intervals
numInterval = int(len(mem) / lenInterval)
#trim membrane data
memCut = mem[:numInterval * lenInterval]
#split membrane data into intervals
memInterval = memCut.reshape(numInterval, lenInterval)
#average membrane data
#note that first and last interval are omitted, because without stimulus
memAverage = np.mean(memInterval[1:-1], axis=0)

##plot results
plt.figure()
plt.plot(timeNorm[:lenInterval], memInterval[1], 'b')
plt.plot(timeNorm[:lenInterval], memAverage, 'r')
plt.legend(['single EPSP', 'average across {} EPSPs'.format(numInterval)])
plt.xlabel('time (ms)')
plt.ylabel('membrane voltage (mV)')
plt.savefig('epsp.png')
