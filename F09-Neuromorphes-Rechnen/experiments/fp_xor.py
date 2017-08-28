#!/usr/bin/env python

'''
XOR Network 
'''

from pylab import *
close('all')
# for plotting without X-server
# import matplotlib as mpl
# mpl.use('Agg')

# load PyNN interface for the Spikey neuromorphic hardware
import pyNN.hardware.spikey as sim

####################################################################
# experiment parameters
# in biological time and parameter domain
####################################################################

runtime = 4000.0 # ms -> 0.1ms on hardware

InputNeuronParams = {
    'v_reset'   : -70.0, # mV shared
    'e_rev_I'   : -80.0, # mV shared
    'v_rest'    : -54.0, # mV shared
    'v_thresh'  : -50.0, # mV shared
    'g_leak'    :  20.0, # nS  -> tau_mem = 0.2nF / 20nS = 10ms individual
    #'tau_refrac':  5.    # ms, shared
}

HiddenNeuronParams = InputNeuronParams
OutNeuronParams = InputNeuronParams

i1spkt = concatenate((arange(1000., 2000., 100.), arange(3000., 4000., 100.)))
i2spkt = concatenate((arange(2000., 3000., 100.), arange(3000., 4000., 100.)))

####################################################################
# procedural experiment description
####################################################################

# necessary setup
sim.setup()

we = sim.minExcWeight() # 
wi = sim.minInhWeight() # 

# set up network

# I want another neuron, so I need to build some dummy neurons, because
sim.Population(193, sim.IF_facets_hardware1, InputNeuronParams)

# create & record neurons
labels = ['i1', 'i2', 'y1', 'y2', 'h1', 'h2', 'o']
popsize = 1
skipsize = 2
populations = {}
parrotsE = {}
parrotsI = {}

# stimuli
populations['i1'] = sim.Population(popsize, sim.SpikeSourceArray, {'spike_times':i1spkt})
populations['i2'] = sim.Population(popsize, sim.SpikeSourceArray, {'spike_times':i2spkt})

# neurons
for label in labels[2:]:
	# wtf workaround for crappy neurons
	if label=='h1':
		sim.Population(1, sim.IF_facets_hardware1, InputNeuronParams)
	if label=='o':
		sim.Population(2, sim.IF_facets_hardware1, InputNeuronParams)
	populations[label] = sim.Population(popsize, sim.IF_facets_hardware1, InputNeuronParams)
	# skip some neurons to reduce crosstalk
	sim.Population(skipsize, sim.IF_facets_hardware1, InputNeuronParams)
	# now the excitatory parrot neurons
	parrotsE[label] = sim.Population(popsize, sim.IF_facets_hardware1, InputNeuronParams)
	# skip some neurons to reduce crosstalk
	sim.Population(skipsize, sim.IF_facets_hardware1, InputNeuronParams)
	# now the inhibitory parrot neurons
	parrotsI[label] = sim.Population(popsize, sim.IF_facets_hardware1, InputNeuronParams)
	# skip some neurons to reduce crosstalk
	sim.Population(skipsize, sim.IF_facets_hardware1, InputNeuronParams)

# parrot neuron connections
for label in labels[2:]:
	sim.Projection(populations[label], parrotsE[label], sim.AllToAllConnector(weights=15*we), target="excitatory")
	sim.Projection(populations[label], parrotsI[label], sim.AllToAllConnector(weights=15*we), target="excitatory")
	sim.Projection(parrotsI[label], populations[label], sim.AllToAllConnector(weights=15*wi), target="inhibitory")
	sim.Projection(parrotsI[label], parrotsE[label], sim.AllToAllConnector(weights=15*wi), target="inhibitory")
	# inhibitory parrots kill themselves
	sim.Projection(parrotsI[label], parrotsI[label], sim.AllToAllConnector(weights=15*wi), target="inhibitory")
	
# 1st layer is stimulated by background
sim.Projection(populations['i1'], populations['y1'], sim.AllToAllConnector(weights=10*we), target="excitatory")
sim.Projection(populations['i2'], populations['y2'], sim.AllToAllConnector(weights=10*we), target="excitatory")

# 2nd layer
sim.Projection(parrotsE['y1'], populations['h1'], sim.AllToAllConnector(weights=11*we), synapse_dynamics=None, target="excitatory")
sim.Projection(parrotsE['y2'], populations['h2'], sim.AllToAllConnector(weights=11*we), synapse_dynamics=None, target="excitatory")
sim.Projection(parrotsE['h1'], populations['o'], sim.AllToAllConnector(weights=11*we), synapse_dynamics=None, target="excitatory")
sim.Projection(parrotsE['h2'], populations['o'], sim.AllToAllConnector(weights=11*we), synapse_dynamics=None, target="excitatory")
sim.Projection(parrotsI['y1'], populations['h2'], sim.AllToAllConnector(weights=15*wi), target="inhibitory")
sim.Projection(parrotsI['y2'], populations['h1'], sim.AllToAllConnector(weights=15*wi), target="inhibitory")

for label in labels:
	populations[label].record()
vlabel = 'o'
sim.record_v(populations[vlabel][0], '')
#sim.record_v(parrotsE[vlabel][0], '')
#sim.record_v(parrotsI[vlabel][0], '')

# execute the experiment
sim.run(runtime)

# evaluate results
spiketrains = {}
for label in labels:
	spiketrains[label] = populations[label].getSpikes()
	print(label, "spike rate: ", len(spiketrains[label])/runtime, "kHz")

vm = sim.membraneOutput
tm = sim.timeMembraneOutput

sim.end()

####################################################################
# data visualization
####################################################################

print 'average membrane potential:', mean(vm), 'mV'
print 'sampling step for membrane potential:', tm[1] - tm[0], 'ms'

colors = ['k', 'm', 'g', 'r', 'b', 'y', 'c']

# draw raster plot
fig = figure()
ax = fig.add_subplot(211) #row, col, nr
h = 0
for label in labels:
	ax.vlines(spiketrains[label], 2*h, 2*h+1, label=label, color=colors[h])
	h+=1
ticks = arange(0,2*len(labels),2) + .5
ax.set_yticks(ticks)
ax.set_yticklabels(labels)
ax.set_ylim(-1, 2*len(labels))
ax.set_xlim(tm[0], tm[-1])
#ax.legend()
	
# draw membrane potential
ax = fig.add_subplot(212)
ax.plot(tm, vm)
ax.set_xlabel('time (ms)')
ax.set_ylabel('vm(' + vlabel + ') [mV]')

savefig('xor.png')
show()
