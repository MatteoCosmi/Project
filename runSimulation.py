# -*- coding: utf-8 -*-
"""
Created on Mon May  3 09:44:58 2021

@author: matte
"""

import SIRmodel as SIR
import utility as ut

def runSim(df, regionalCode: int, net: SIR.Network, model: SIR.SirModel):
    subdf = ut.usefulCols(df[df['codice_regione']==regionalCode])
    