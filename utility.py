# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:58:38 2021

@author: matte
"""
import pandas as pd
import numpy as np

def getRegionName(df, rc):
    names = df[df['codice_regione']==rc]['denominazione_regione']
    if len(np.unique(names))>1:
        print("clean data: more region with a same code")
        #code_url = "http://www.salute.gov.it/imgs/C_17_pubblicazioni_1049_ulterioriallegati_ulterioreallegato_0_alleg.txt"
        #codedf = pd.read_csv(code_url, header = 0, delimiter = "\t")
    else:
        return np.unique(names)[0]

def filterCols(df):
    return df[['data', 'ricoverati_con_sintomi', 'terapia_intensiva', 'totale_ospedalizzati',
              'isolamento_domiciliare', 'totale_positivi', 'variazione_totale_positivi',
              'nuovi_positivi', 'dimessi_guariti', 'deceduti', 'totale_casi', 'tamponi',
              'casi_testati', 'ingressi_terapia_intensiva', 'totale_positivi_test_molecolare',
              'totale_positivi_test_antigenico_rapido', 'tamponi_test_molecolare', 'tamponi_test_antigenico_rapido']]

def usefulCols(df):
    return df[['data', 'nuovi_positivi', 'dimessi_guariti', 'deceduti', 'totale_positivi','totale_casi', 'tamponi']]