# -*- coding: utf-8 -*-
"""
Created on Mon May  3 15:59:55 2021

@author: matte
"""

import SIRmodel as SIR

def fitBeta(subdf, pop, betalist,p_edges, startingNodes, N, I0, gamma, vaxAvailability, vaxDailyIncrease, LD):
    pos = list(subdf['totale_positivi'])
    scale = round(pop/N)
    starting = next(i for i,v in enumerate(pos) if v>=scale)
    #Building Network
    net = SIR.Network("net1", N,10/N, 'Central', 1/N, False)
    for beta in betalist:
        model = SIR.SirModel('beta{}'.format(beta), beta,gamma,'Central', vaxAvailability, vaxDailyIncrease, False, False, 21)
        it, inf, cumav = SIR.covidSir(net, model)
    
def MSE(simulation, measured):
    return np.mean(list(map(lambda x: (simulation[x]*scale-measured[x])^2, range(0,len(simulation)))))

popReg = {"1":4311217,
          "2":125034,
          "3":10027602,
          "4":1078069,
          "5":4879133	,
          "6":1206216,
          "7":1524826,
          "8":4464119,
          "9":3692555,
          "10":870165,
          "11":1512672,
          "12":5755700,
          "13":1293941,
          "14":300516,
          "15":5712143,
          "16":3953305,
          "17":553254,
          "18":1894110,
          "19":4875290,
          "20":1611621,
          "21":532644,
          "22":545425
    }