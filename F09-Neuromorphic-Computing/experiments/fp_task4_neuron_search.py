#!/usr/bin/env python

'''
Fortgesschrittenenpraktikum F09/10 - Neuromorphic Computing
Task 4 - Short Term Plasticity

Andreas Gruebl, July 2016, agruebl@kip.uni-heidelberg.de

This network demonstrates short-term plasticity (STP) on hardware.
The postsynaptic neuron is stimulated by a single input with STP enabled.
For high input rates the impact of each presynaptic spike on the membrane potential decreases.
For low input rates the synaptic efficacy recovers.
'''

# for plotting without X-server
import matplotlib as mpl
mpl.use('Agg')

import pyNN.hardware.spikey as pynn
import numpy as np

for i in range(1,50):
	for j in range(1,50):
		# row and column of synapse
		# you can play around with these parameters to find a "nice" synapse...
		row = i #59
		column = j #42

		weight = 15.0

		dist = 150.0
		final = 600.0

		stimParams = {'spike_times': np.concatenate((np.arange(100.0, 401.0, dist), [final]))}
		# STP parameters (depression and facilitation cannot be enabled simultaneously!):
		# U: Usable synaptic efficacy (U_SE, see script) - scales the size of PSPs. 0.4
		# tau_rec: time constant of short term depression 100.0
		# tau_facil: time constante of short term facilitation 0.0
		stpParams = {'U': 40.0, 'tau_rec': 0.0, 'tau_facil': 300.0} # U =1.4
		runtime = 1000.0

		pynn.setup(mappingOffset=column)

		neuron = pynn.Population(1, pynn.IF_facets_hardware1)
		dummy = pynn.Population(row, pynn.SpikeSourceArray, stimParams)
		stimulus = pynn.Population(1, pynn.SpikeSourceArray, stimParams)

		# enable and configure STP
		stp_model = pynn.TsodyksMarkramMechanism(**stpParams)
		pynn.Projection(stimulus, neuron,
						method=pynn.AllToAllConnector(weights=weight * pynn.minExcWeight()),
						target='excitatory',
						synapse_dynamics=pynn.SynapseDynamics(fast=stp_model))

		pynn.record_v(neuron[0], '')

		pynn.run(runtime)

		membrane = np.array(zip(pynn.timeMembraneOutput, pynn.membraneOutput))

		pynn.end()

		# plot
		import matplotlib.pyplot as plt
		plt.plot(membrane[:,0], membrane[:,1])
		plt.xlabel('time (ms)')
		plt.ylabel('membrane potential (mV)')
		plt.title('STP with distance={} and final spike at {}'.format(dist, final))
		plt.savefig('{}-{}.png'.format(i, j))
		plt.close()
