# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:35:26 2020

@author: KDD2070

測試用，貌似沒有用途

"""

import pickle
with open("train_data_discretization.pickle", "rb") as fp:   # Unpickling
    train_data_discretization = pickle.load(fp)
with open("val_data_discretization.pickle", "rb") as fp:   # Unpickling
    val_data_discretization = pickle.load(fp)
#%%
with open("subject_episode_hadm_icu.pickle", "rb") as fp:   # Unpickling
    subject_episode_hadm_icu = pickle.load(fp)
hadm=[]
for i in subject_episode_hadm_icu:
    for j in subject_episode_hadm_icu[i]:
        hadm.append(j[1])
print(set(hadm))
#%%
with open('all_stays.csv',newline='',encoding='utf-8') as r:
    hadm=[]
    headers = next(r)
    for line in r:
        line=line.strip()
        line = line.split(',')
        hadm.append(line[1])#hadm = 42276