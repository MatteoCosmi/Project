# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:48:52 2021

@author: matte
"""

import networkx as nx
import random
import pylab as plt
import numpy as np
import time
import copy
import epyestim.covid19 as covid19
import pandas as pd
from datetime import datetime


class Network:
   netCount = 0
   def __init__(self, name, N, p_edges, startingNodes, percI0, plot):
      self.name = name
      self.N = N
      self.p_edges = p_edges
      self.startingNodes = startingNodes
      self.percI0 = percI0
      self.plot = plot
      Network.netCount += 1
   
   def displayCount(self):
     print("Total Num Tested Networks %d" % Network.netCount)

   def displayNetworks(self):
      print("Name : ", self.name,  ", N: ", self.N,  ", p_edges: ", self.p_edges,  ", Starting Nodes: ", self.startingNodes,  ", I0: ", self.percI0)

class SirModel:
   sirCount = 0
   def __init__(self, name, beta, gamma,strategy, VaxAvailability, dailyVaccineIncrease, lockdownStrategy,plot,maxIt):
      self.name = name
      #self.G = G
      self.beta = beta
      self.gamma = gamma
      self.strategy = strategy
      self.VaxAvailability = VaxAvailability
      self.percIncreaseVax = dailyVaccineIncrease
      self.lockdownStrategy = lockdownStrategy
      self.plot = plot
      self.maxIt = maxIt
      SirModel.sirCount += 1
   
   def displayCount(self):
     print("Total Num Tested Sir Models %d" % SirModel.sirCount)

   def displaySirModels(self):
      print("Name : ", self.name,  ", strategy: ", self.strategy,  ", VaxAvailability: ", self.VaxAvailability,  ", percIncreaseVax: ", self.dailyVaccineIncrease, ",lockdownStrategy:", self.lockdownStrategy)



def initialise(graph, startingNodes:str, perc:float,plot:bool):
    G = graph
    numneighList = list(map(lambda x: len(list(G.neighbors(x))),G.nodes()))
    sortednumneigh = np.argsort(numneighList)[::-1]
    if startingNodes == 'Perifery':
        infected = sortednumneigh[-round(perc*G.number_of_nodes()):]
    elif startingNodes == 'Central':
        infected = sortednumneigh[0:round(perc*G.number_of_nodes())]    
    for g in G.nodes():
        if g in infected:
            G.nodes[g]['category'] ='I'
        else:
            G.nodes[g]['category'] ='S'
        
    if plot == True:
        color_map = {'S':'b', 'I':'r', 'R':'g', 'V':'y'}
        POS = nx.spring_layout(G)
        nx.draw(G, POS, node_color=[color_map[G.nodes[node]['category']] for node in G])
        plt.show()
    return G

def isgInfected(p,numIneigh):
    if random.uniform(0, 1) >= (1-p)**numIneigh:
        return 'I'
    else:
        return 'S'
    
def isgStillInfected(g,q):
    if random.uniform(0, 1) >= q:
        return 'I'
    else:
        return 'R'
    
def getInfectedNum(G,Neigh='ALL'):
    if Neigh=='ALL':
        return list(map(lambda x: G.nodes()[x]['category']=='I',G.nodes()))
    else:
        return list(map(lambda x: G.nodes()[x]['category']=='I',Neigh))
   
    
def getVaccine(G, sortedG:list,strategy:str, availability:int):
    if availability>0:
        #infected = list(map(lambda x: G.nodes()[x]['category']=='I',G.nodes()))
        susc =  list(map(lambda x: G.nodes()[x]['category']=='S',G.nodes()))
        if strategy=='Central':
            tbv = []
            pos = 0
            while len(tbv)< availability and len(tbv)<sum(susc):
                if susc[sortedG[pos][0]]:
                    tbv.append(sortedG[pos][0])
                pos +=1
        else:
            possusc = [i for i,x in enumerate(susc) if x == True]
            tbv = random.sample(possusc, max(availability, len(possusc)))
        for g in tbv:
                G.nodes()[g]['category']='V'
    return G

def lockdownReductions(typeofLD:str):
    if typeofLD=="yellow":
        return -0.1, -0.02#-0.1, -0.05#
    elif typeofLD =="orange":
        return -0.15, -0.05
    elif typeofLD =="red":
        return -0.4, -0.1
    elif typeofLD =="white": #end of LD
        return +0.2, +0.0
    

def lockdown(G, startingG, typeofLD:str):
    redE, redp = lockdownReductions(typeofLD)
    #neigh = G.degree
    #newneigh = {i[0]: int(round(i[1]*(1+redE))) for i in neigh}
    for i in range(0, len(G.nodes())):
        if i == 0:
                #status = [G.nodes()[i] for i in G.nodes()]
                G.remove_edges_from(G.edges())
                G.add_edges_from(startingG.edges())
        neigh = G.degree(i)
        newneigh = int(round(neigh*(1+redE)))
        candidates = list(G.neighbors(i))
        if neigh>newneigh:
            remove = random.sample(candidates, neigh-newneigh)
            for j in remove:
                G.remove_edge(i,j)
        else:
            add = random.sample(list(set(range(0, len(G.nodes()))) - set(candidates)), newneigh-neigh)
            for j in add:
                G.add_edge(i,j)
    return G, redp
            
def chooseLDstrategy(Rt):
    if  0.5 <= Rt < 1.25:
        return "yellow"
    elif 0.5 < Rt < 1.5:
        return "orange"
    elif Rt > 1.5:
        return "red"
    else:
        return "white"    
        
def computeRt(inf, TimeInterval = 7, firstDay=None):
    if firstDay==None:
        firstDay = datetime.today()
    datelist = pd.date_range(firstDay, periods=len(inf)).tolist()
    rtinput = pd.Series(inf, index=datelist)
    Rts =  covid19.r_covid(rtinput, smoothing_window=min(21,len(rtinput)),r_window_size=min(len(rtinput),TimeInterval), auto_cutoff = False)['R_mean']
    if len(Rts)>0:
        return Rts[len(Rts)-1]
    else:
        return 0


def evolution(G_er, model):
    G = copy.deepcopy(G_er)
    startingG = copy.deepcopy(G)
    sortedG = sorted(nx.degree_centrality(G).items(), key=lambda item: item[1], reverse=True)
    iterations = 0
    infections = [sum(getInfectedNum(G,Neigh='ALL'))]
    cumav = [model.VaxAvailability]
    color = 'white'
    cumcolors = [color]
    if model.plot==True:
        color_map = {'S':'b', 'I':'r', 'R':'g', 'V':'y'}
        POS = nx.spring_layout(G)
        nx.draw(G, pos= POS, node_color=[color_map[G.nodes[node]['category']] for node in G])
        plt.show()
        time.sleep(0.0001)
    while sum(getInfectedNum(G))>0 and iterations < model.maxIt:
        #print(iterations)
        G_copy = copy.deepcopy(G)
        for g in G.nodes():
            if G_copy.nodes()[g]['category'] == 'S':
                neigh = list(G_copy.neighbors(g))
                Ineigh = getInfectedNum(G_copy,Neigh=neigh)
                numIneigh = sum(Ineigh)
                G.nodes()[g]['category'] = isgInfected(model.beta,numIneigh)                    
            elif G_copy.nodes()[g]['category'] == 'I':
                G.nodes()[g]['category'] =isgStillInfected(g,model.gamma)
        if model.plot==True:
                nx.draw(G, pos= POS, node_color=[color_map[G.nodes[node]['category']] for node in G])
                plt.show()
                time.sleep(0.0001)
        infections.append(sum(getInfectedNum(G,Neigh='ALL')))
        iterations += 1
        model.VaxAvailability =int(np.ceil(model.VaxAvailability*(1+model.percIncreaseVax)))
        cumav.append(model.VaxAvailability)
        if model.lockdownStrategy and iterations > 1 and (iterations-1) % 7 == 0:
            Rt = computeRt(infections, TimeInterval = 7, firstDay=None)
            print(Rt)
            new_color = chooseLDstrategy(Rt)
            cumcolors.append(new_color)
            print(new_color)
            if color != new_color:
                color = new_color
                G,redp = lockdown(G, startingG, color)
                model.beta = model.beta*(1+redp)
        G = getVaccine(G,sortedG, model.strategy, model.VaxAvailability)
        
    return iterations, infections, cumav

def covidSir(net: Network, Sir: SirModel):
    G_er = initialise(nx.erdos_renyi_graph(net.N,net.p_edges), net.startingNodes, net.percI0,net.plot)
    it, inf, cumav = evolution(G_er, Sir)
    return it, inf, cumav
 
