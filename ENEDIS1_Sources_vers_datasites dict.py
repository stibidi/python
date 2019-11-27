#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import glob
import pickle

os.chdir('C:/BMT/csv_python/IP3/source')

listCSV = glob.glob("CDC/*.csv")
listPRM = []
datasites = {}

listadmcons = glob.glob("CSV/*.csv")
dfdict = {}
dfdict_adm = {}
dfdict_cons = {}
listadm = []

# ========================== lire les csv SGE (admin et conso) et créer df_ adm et cons =======================
for h in listadmcons: 
    key_nm = 'df_admcons_'+str(h)[-17:-4]
    dfdict[key_nm] = pd.read_csv(h, delimiter=";",encoding='ANSI')
    key_nm_adm = 'dfdict_adm_'+str(h)[-17:-4]
    key_nm_cons = 'dfdict_cons_'+str(h)[-17:-4]
    if (dfdict[key_nm].columns.values[1] == "Esc-etage-appt") == True:
        dfdict_adm['admin_sites'] = dfdict[key_nm]
    if (dfdict[key_nm].columns.values[1] == "Type Grille") == True:
        dfdict_cons['conso_sites'] = dfdict[key_nm]


# =============================== lire les csv de CDC 1 par 1 (f)================
for f in listCSV: 
    df = pd.read_csv(f, delimiter = ";", encoding='ANSI')
    prm = str(int(df['PRM'][0]))
    listPRM.append(prm)
    cdc = pd.read_csv(f, delimiter = ";", encoding='ANSI', usecols=[0,1,2], parse_dates=[['Date de la mesure', 'Heure de la mesure']])
    Nkeys = ["cdc","infos_sites","admin_sites","conso_sites"]
    datasites[prm] = {}
    datasites[prm]["cdc"] = cdc

    # ===== lire la liste manuelle des noms_sites par PRM et rajouter la bonne ligne au bon PRM =====    
    with open("sites.csv") as g: 
        df_inf=pd.read_csv(g)
    df_inf = df_inf[(df_inf["PRM"] == int(prm))]
    datasites[prm]["infos_sites"] = df_inf
    
    # ====== Rajouter a datasites les infos PRM de CSV Admin ======================
    datasites[prm]['admin_sites'] = pd.DataFrame()
    dfadm = dfdict_adm['admin_sites']
    df_adm = dfadm[dfadm['PRM'] == int(prm)]
    datasites[prm]['admin_sites'] = df_adm
    
    # ====== Rajouter a datasites les infos PRM de CSV consos ======================
    datasites[prm]['conso_sites'] = pd.DataFrame()
    dfcons = dfdict_cons['conso_sites']
    df_cons = dfcons[dfcons['PRM'] == int(prm)]
    datasites[prm]['conso_sites'] = df_cons
       
#print('sortie de boucle : \n',datasites,'\n')

PRMs = list(datasites.keys())

df_cdc_PRM1 = pd.DataFrame()
df_cdc_PRM1 = datasites[PRMs[0]]['cdc']
df_cdc_PRM1 = df_cdc_PRM1.rename(columns={"Date de la mesure_Heure de la mesure":"H10","Valeur":"P10"})


with open('datasites_test1.pickle', 'wb') as datafile :
    pickle.dump(datasites, datafile)
