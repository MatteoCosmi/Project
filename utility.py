# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:58:38 2021

@author: matte
"""

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