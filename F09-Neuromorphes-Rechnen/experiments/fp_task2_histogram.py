#!/usr/bin/env python
import numpy as np
'''
Fortgesschrittenenpraktikum F09/10 - Neuromorphic Computing
Task 2 - Calibrating Neuron Parameters

Andreas Gruebl, July 2016, agruebl@kip.uni-heidelberg.de
'''


####################################################################
# experiment parameters
# in biological time and parameter domain
####################################################################

runtime = 200.0 # ms -> 0.1ms on hardware

neuronParams = {
    'v_reset'   : -80.0, # mV 
    'e_rev_I'   : -75.0, # mV
    'v_rest'    : -50.0, # mV
    'v_thresh'  : -61.0, # mV  - default value. Change to result of your calculation!
    'g_leak'    :  20.0  # nS  -> tau_mem = 0.2nF / 20nS = 10ms
}

####################################################################
# procedural experiment description
####################################################################

# for plotting without X-server
import matplotlib as mpl
mpl.use('Agg')

# load PyNN interface for the Spikey neuromorphic hardware
import pyNN.hardware.spikey as pynn

# necessary setup
pynn.setup(calibTauMem=False)

# set up one neuron
# create neurons

neurons = []
for i in range(192):
	neurons.append(pynn.Population(1, pynn.IF_facets_hardware1, neuronParams)) 


# increase refractory period by reducing hardware parameter icb
pynn.hardware.hwa.setIcb(0.2)

# individually set leakage conductance:
# already set to default value

#gs = []
#for i in range(192):
#	gs.append(20.0)

#gs = [20.0, 18.963262545374565, 16.115044181969967, 10.439269082121358, 16.578093570801478, 20.329332945873084, 37.699807978679765, 10.180293146284683, 31.012239953055676, 19.043137204489096, 19.863648136739389, 23.063903251896608, 17.599516714371124, 7.7324835548894821, 24.978105921576486, 21.873872738217301, 17.843222049838655, 20.460673113812014, 22.042365095735754, 15.602202560397203, 30.815439989710207, 16.322688767889971, 22.532058829274145, 24.518900885989588, 21.772825676461927, 31.678172277475092, 29.182692679241654, 23.222104436289861, 16.639634144607896, 17.679611035243109, 21.469452598362547, 31.020495530409839, 22.0788091963637, 15.740679897325089, 16.740017177644514, 24.761471818222439, 16.568665589657382, 20.409077046695906, 10.584132689676039, 8.8992057069735413, 13.033742091911089, 13.049865623328152, 23.346154143393324, 27.778805446034557, 27.946286156206959, 32.534945237756368, 19.123686537607568, 23.560108159832318, 17.153958725032524, 18.988528751476665, 12.991676787266385, 9.8799595820581789, 28.722397395672843, 23.465234096472301, 18.164587533415464, 13.116445850809349, 17.353185541348125, 25.157278658655173, 28.053920647992314, 31.669563553373905, 14.601374103750985, 29.545699349132249, 19.612276812870878, 27.128491987897885, 20.769888357070808, 17.60365135768533, 19.606997680448501, 18.074441023411428, 29.159326852841065, 27.725938407261165, 17.356632203251031, 29.714440498602205, 20.997405912300415, 26.556250356712077, 30.342096867984552, 16.517006169851015, 13.94956836452306, 18.529112782897876, 24.704409031254627, 13.045969903291162, 25.163964051775622, 21.713819999282187, 26.071584535285023, 23.674971685276166, 39.597203479307069, 22.229907684752032, 27.583446420937754, 27.19360031718751, 28.046203179530135, 17.698703514801657, 24.781993379259056, 13.622228346664699, 24.217901980141242, 11.64818741957424, 27.710869976337346, 22.892571745493377, 34.612460864105088, 12.515463927661541, 29.776187945868337, 41.579655392654786, 33.126805221547016, 15.224843227216178, 34.796178242750038, 23.252992402435201, 20.558847315455345, 23.414946891045805, 12.515463449140727, 33.658059179051428, 34.268687287181741, 18.64505082278523, 22.349790373606663, 23.842879305099952, 17.570623878748947, 34.268688354914623, 8.0021967877997504, 16.017592046104415, 27.186349351658091, 26.702276739661663, 30.239750816923276, 14.839347535789988, 36.709812424283925, 11.620313530206698, 30.14900608583687, 21.498256290766861, 22.360706338270148, 30.71797467690989, 22.69748111677152, 22.7092750683593, 22.207317053636682, 11.60242116008604, 56.37770785992339, 17.425836912520939, 17.613110591571857, 28.767772027262815, 20.340686878810072, 28.602094156800391, 22.46887265945794, 24.293496753075466, 18.134438870199936, 25.461682794259289, 23.050631734771351, 31.153168094972244, 34.134859018859004, 26.501038988265556, 12.612986497469231, 22.188867318195179, 24.487199684646754, 17.058547382961386, 20.816834808811681, 31.980370289656893, 17.78995868279199, 21.550296159233806, 27.986678938806659, 14.489343070441002, 21.981892215843104, 18.044590281446371, 30.693705957401335, 18.963262231493584, 21.04096529428513, 19.538625606291941, 18.930407159015946, 15.988710816785176, 31.704025484709774, 30.742283747154282, 10.611887534370066, 28.453125364525491, 7.6272251902002788, 19.989023009534066, 28.438313279947582, 18.301507153659596, 44.818618028733027, 8.8910587070034186, 23.547412937770609, 15.651893611708354, 30.987501735567232, 12.678851153379188, 37.068700421813531, 29.331542094928189, 21.429258067498456, 25.257934613444238, 15.543344851975906, 29.24518053577534, 36.905599304199221, 25.393402993996247, 21.512108616532647, 29.934246010976299, 17.622580855049037, 29.975309017960321, 37.106470125379879, 16.970229811189647, 22.899113625816824, 18.979732571619088]

#for i in range(192):
#	neurons[i].set({'g_leak' : round(gs[i],1)})
#print(gs)

# define which observables to record
for item in neurons:
	item.record()

# execute the experiment
pynn.run(runtime)
	
# membrane potential
# when recording more than one membrane voltage, the on-board ADC cannot be used, anymore!
# (it will record a flat line). Instead, only oscilloscope recordings are possible.
#pynn.record_v([neuron1[0], neuron2[0], neuron3[0], neuron4[0]], '')

diff_spikes = []
diff_means = []
print('Test1')
for j in range(len(neurons)):
	tmp = neurons[j].getSpikes()[:,1]
	for i in range(len(tmp)-1):
		tmp[i] = tmp[i+1] - tmp[i]	
	diff_spikes.append(np.delete(tmp, -1))
	diff_means.append(np.mean(np.delete(tmp, -1)))
	#gs[j] = diff_means[0]/diff_means[j]*gs[j]
print('Test2')	


print(np.std(diff_means))


	
diff_data = np.hstack((diff_means))
#print(diff_data)
#print(diff_means)
pynn.end()



import matplotlib.pyplot as plt
n, bins, patches = plt.hist(diff_data, 20, facecolor='green', alpha=0.75)
plt.xlabel(r'$\tau_m[ms]$')
plt.ylabel(r'$Neurons$')
plt.title(r'Calibrating Neuron Parameters - Distribution of firing rates (192 neurons)')
plt.grid(True)
plt.show()
plt.savefig('histogramm.png')

#x_lst = range()
f = open('2-4-histogram.txt', 'w')
for i in range(len(diff_data)):
	f.write(str(diff_data[i])+'\n')
f.close()


'''
print('Test')
print(neurons[30][0])

#A4.2.4
neurons_0 = []
for i in range(0, len(neurons)):
	neurons_0.append(neurons[i][0])
	
pynn.record_v(neurons_0, '')

#print(neurons_0)
'''
'''

# execute the experiment
pynn.run(runtime)

# evaluate results
print(neuron1.getSpikes())
#spikes1 = neuron1.getSpikes()[:,1]
#spikes2 = neuron2.getSpikes()[:,1]
#spikes3 = neuron3.getSpikes()[:,1]
#spikes4 = neuron4.getSpikes()[:,1]



frequencies = []
for i in neurons:
	spikes = i.getSpikes()[:,1]
	
	diff = []
	for i in range(len(spikes)-1):
		diff.append(spikes[i+1]-spikes[i])
	
	differences = np.array(diff)/1000	
	freq = 1/(np.array(diff)/1000)
	frequencies.append(np.mean(freq))
	print(np.mean(freq))

membrane = pynn.membraneOutput
membraneTime = pynn.timeMembraneOutput

pynn.end()

####################################################################
# data visualization
####################################################################

import numpy as np
print 'average membrane potential:', np.mean(membrane), 'mV'
print 'sampling step for membrane potential:', membraneTime[1] - membraneTime[0], 'ms'

import matplotlib.pyplot as plt

# draw raster plot
#ax = plt.subplot(211) #row, col, nr
for spike in spikes1:
    ax.axvline(x=spike)
ax.set_xlim(0, runtime)
ax.set_ylabel('spikes')
ax.set_xticklabels([])
ax.set_yticks([])
ax.set_yticklabels([])

# draw membrane potential
axMem = plt.subplot(212)
axMem.plot(membraneTime, membrane)
axMem.set_xlim(0, runtime)
axMem.set_xlabel('time (ms)')
axMem.set_ylabel('membrane potential (mV)')

plt.savefig('example.png')

plt.hist(frequencies)
plt.savefig('histogram.png')
'''
