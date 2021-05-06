# -*- coding: utf-8 -*-
"""
Created on Mon May  3 09:44:58 2021

@author: matte
"""

import SIRmodel as SIR
import utility as ut
import fittingBeta as fB
import numpy as np
from datetime import datetime

def runSim(df, regionalCode: int, net: SIR.Network, model: SIR.SirModel, betalist: list):
    subdf = ut.usefulCols(df[df['codice_regione']==regionalCode])
    pop = ut.popReg[str(regionalCode)]
    results, RMSEs, data, dates = fB.fitBeta(subdf, pop, betalist,model.maxIt,net.p_edges, net.startingNodes, net.N, net.percI0, model.gamma, model.VaxAvailability, model.percIncreaseVax, model.lockdownStrategy)
    min_index = np.argmin(RMSEs)
    bestRes = results[min_index]
    fB.plotRMSEs(RMSEs,betalist)
    fB.plotResults(bestRes, data)
    bestBeta = betalist[min_index]
    return results,RMSEs, bestBeta

def runSecondWave(df, start, end, regionalCode:int, net: SIR.Network, model:SIR.SirModel):
    subdf = ut.usefulCols(df[df['codice_regione']==regionalCode])
    pop = ut.popReg[str(regionalCode)]
    starting = next(i for i,v in enumerate(subdf['data']) if datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')>=datetime.strptime(start, '%d/%m/%y %H:%M:%S'))
    ending = next(i for i,v in enumerate(subdf['data']) if datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')==datetime.strptime(end, '%d/%m/%y %H:%M:%S'))
    data = list(subdf['totale_positivi'])[starting:ending]
    percI0 = max(1/net.N,data[0]/pop)
    net.percI0 = percI0
    model.maxIt = ending-starting-1
    it, inf, cumav = SIR.covidSir(net, model)
    if len(inf)<ending-starting:
        inf.extend(np.zeros(ending-starting-len(inf), dtype=int))
    res = [int(round(i*pop/net.N)) for i in inf]
    rmse = fB.RMSE(res, data)
    fB.plotResults(res, data)
    return rmse,res, data
