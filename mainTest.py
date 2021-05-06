# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import utility as ut
import SIRmodel as SIR
import runSimulation as rs

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
beta = 0.02
gamma = 0.1

#Plot settings
plot = False

#Vaccine Availability
vaxAvailability = 0
vaxDailyIncrease = 0.002
#Lockdown
LD = True


#Build Network
net = SIR.Network("net1", 50000,1/5000, 'Central', 2/100000, False)
#Build Model
model = SIR.SirModel('noVaxnoLock', beta,gamma,'Central', vaxAvailability, vaxDailyIncrease, False, False, 210)
#Run Simulation
#it, inf, cumav = SIR.covidSir(net, model)

#Set parameters to fit model to data
betalist=[0.005,0.015,0.025,0.035,0.045]
model.maxIt = 21

#Choose Italian region
regionName = 'Lazio'
regionalCode = list(regionNames.keys())[list(regionNames.values()).index(regionName)]

#Run Simulation (first 21 days of COVID-19 outbreak)
SIR_res, SIR_RMSEs, beta = rs.runSim(df, regionalCode, net, model, betalist)

#Test model from March to September
start = '01/03/20 17:00:00'
end = '01/06/20 17:00:00'
model.beta = beta
model.lockdownStrategy=False
model.VaxAvailability = 0
rmse, res, data = rs.runSecondWave(df, start, end, regionalCode, net, model)

#Test Model on second outbreak of COVID-19 wave
start = '01/09/20 17:00:00'
end = '01/11/20 17:00:00'
model.beta = beta
rmse, res, data = rs.runSecondWave(df, start, end, regionalCode, net, model)

#Test Model on second outbreak of COVID-19 (allowing Lockdown)
start = '01/09/20 17:00:00'
end = '01/11/20 17:00:00'
model.lockdownStrategy = LD
rmse_LD, res_LD, data = rs.runSecondWave(df, start, end, regionalCode, net, model)

#Test Model on first outbreak of COVID-19 (allowing Lockdown)
start = '01/03/20 17:00:00'
end = '01/09/20 17:00:00'
model.lockdownStrategy = LD
rmse_LD, res_LD, data = rs.runSecondWave(df, start, end, regionalCode, net, model)

#Test Model first outbreak of COVID-19 (Lockdown and Vaccination)
start = '01/03/20 17:00:00'
end = '01/09/20 17:00:00'

#Network parameters 
N=50000
p_edges = 10/N
startingNodes = 'Central'
I0 = 1/N

#Model hyperparaemeters
beta = 0.02
gamma = 0.015

#Plot settings
plot = False

#Vaccine Availability
vaxAvailability = 1
vaxDailyIncrease = 0.002
#Lockdown
LD = True


#Build Network
net = SIR.Network("net1", N,p_edges, 'Central', I0, plot)
#Build Model
model = SIR.SirModel('VaxLock', beta,gamma,'Central', vaxAvailability, vaxDailyIncrease, LD, plot,  180)

rmse_LD, res_LD, data = rs.runSecondWave(df, start, end, regionalCode, net, model)

