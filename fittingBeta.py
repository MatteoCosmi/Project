# -*- coding: utf-8 -*-
"""
Created on Mon May  3 15:59:55 2021

@author: matte
"""

import SIRmodel as SIR
import numpy as np
import matplotlib.pyplot as plt


def fitBeta(subdf, pop, betalist,endTrain,p_edges, startingNodes, N, percI0,gamma, vaxAvailability, vaxDailyIncrease, LD):
    pos = list(subdf['totale_positivi'])
    scale = round(pop/N)
    starting = next(i for i,v in enumerate(pos) if v>=scale)
    #Building Network
    results = []
    RMSEs = []
    for beta in betalist:
        print("Beta:{}".format(beta))
        net = SIR.Network("net1", N,p_edges, 'Central', percI0, False)
        model = SIR.SirModel('beta{}'.format(beta), beta,gamma,'Central', vaxAvailability, vaxDailyIncrease, False, False, endTrain)
        c=0
        itt = 0
        while c<endTrain/2 and itt<3:
            it, inf, cumav = SIR.covidSir(net, model)
            c = len(inf)
        res = [i*scale for i in inf]
        if len(res)<endTrain:
            res.extend(np.zeros(endTrain+1-len(res), dtype=int))
        results.append(res)
        RMSEs.append(RMSE(res, pos[starting:starting+len(res)]))
    return results, RMSEs, pos[starting:starting+len(res)], subdf['data'][starting:starting+len(res)]
    


def RMSE(simulation, measured):
    return np.sqrt(np.mean(list(map(lambda x: (simulation[x]-measured[x])**2, range(0,min(len(simulation),len(measured)))))))

def chooseBestBetaAndPlot(RMSEs:list, results:list, data:list, dates:list, betalist:list, plot:bool):
    ind = np.argmin(RMSEs)
    y1 = results[ind]
    y2 = list(data)
    x = list(dates)
    if plot:
        plt.plot(x, y1, linewidth=5, linestyle='--', marker='o', label = "SIR")
        plt.plot(x, y2, linewidth=5, linestyle='-.', marker='o', label = "Data")
        plt.ylabel('I(t)')
        plt.xlabel('Day')
        plt.legend(loc='upper left')
        plt.show()
        plt.savefig('BestBetaI(t).png')
        
        plt.plot(betalist, RMSEs, linewidth=5, linestyle='--', marker='o')
        plt.ylabel('RMSE')
        plt.xlabel('Beta')
        plt.show()
        plt.savefig('RMSEs.png')
    
    return ind

def plotRMSEs(RMSEs,betalist):
    plt.plot(betalist, RMSEs, linewidth=5, linestyle='--', marker='o')
    plt.ylabel('RMSE')
    plt.xlabel('Beta')
    plt.show()

def plotResults(result, data):
    y1 = result
    y2 = list(data)
    x = list(range(0,len(result)))
    
    plt.plot(x, y1, linewidth=5, linestyle='--', marker='o', label = "SIR")
    plt.plot(x, y2, linewidth=5, linestyle='-.', marker='o', label = "Data")
    plt.ylabel('I(t)')
    plt.xlabel('Day')
    plt.legend(loc='upper left')
    plt.show()

