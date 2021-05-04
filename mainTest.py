# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

import utility as ut
import SIRmodel as SIR

#Input Data (italian)
url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
df = pd.read_json(url)

regionalCodes = np.unique(df['codice_regione'])
regionNames = {rc: ut.getRegionName(df, rc)  for rc in regionalCodes}

'''
for code in regionalCodes:
    subdf = ut.usefulCols(df[df['codice_regione']==code])
'''

#Network parameters (default)
N=50000
p_edges = 1/5000
startingNodes = 'Central'
I0 = 1/50000

#Model hyperparaemeters
beta = 0.05
gamma = 0.1

t= 'Central'

#Plot settings
color_map = {'S':'b', 'I':'r', 'R':'g', 'V':'y'}
plot = False

#Vaccine Availability
vaxAvailability = 1
vaxDailyIncrease = 0.002
#Lockdown
LD = True

#Build Network
net = SIR.Network("net1", 50000,1/5000, 'Central', 2/100000, False)
#Build Model
model = SIR.SirModel('noVaxnoLock', beta,gamma,'Central', vaxAvailability, vaxDailyIncrease, False, False, 210)
#Run Simulation
it, inf, cumav = SIR.covidSir(net, model)

#Run Simulation (using real data)
