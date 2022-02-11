# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:02:18 2021

@author: KDD204
output:
newlabel_train
newlabel_val
newlabel_test
"""
import pickle
import csv

with open("subject_episode_hadm_icu.pickle", "rb") as fp:   # Unpickling
    subject_episode_hadm_icu = pickle.load(fp) 
with open("subject_episode_hadm_icu_test.pickle", "rb") as fp:   # Unpickling
    subject_episode_hadm_icu_test = pickle.load(fp)

#一個list[],存放順序為trainlist的subject_episode幾的順序，存放格式為hadmid。 
hadm_id_trainlist=[]
hadm_id_vallist=[]
hadm_id_testlist=[]
with open("train_listfile.csv",  newline='') as fp:
    rows = csv.reader(fp)
    headers = next(rows)
    for row in rows:
        a=row[0].split('_')[0]#subject
        b=row[0].split('_')[1]#episode
        id1=-1
        for i in subject_episode_hadm_icu[a]:
            if i[0] == b[7:]:
                id1=i[1]#hadm_id
        if id1 ==-1:
            raise ValueError('ValueError')
        hadm_id_trainlist.append(id1)
with open("val_listfile.csv",  newline='') as fp:
    rows = csv.reader(fp)
    headers = next(rows)
    for row in rows:
        a=row[0].split('_')[0]
        b=row[0].split('_')[1]
        id1=-1
        for i in subject_episode_hadm_icu[a]:
            if i[0] == b[7:]:
                id1=i[1]#hadm_id
        if id1 ==-1:
            raise ValueError('ValueError')
        hadm_id_vallist.append(id1)
with open("test_listfile.csv",  newline='') as fp:
    rows = csv.reader(fp)
    headers = next(rows)
    for row in rows:
        a=row[0].split('_')[0]
        b=row[0].split('_')[1]
        id1=-1
        for i in subject_episode_hadm_icu_test[a]:
            if i[0] == b[7:]:
                id1=i[1]#hadm_id
        if id1 ==-1:
            raise ValueError('ValueError')
        hadm_id_testlist.append(id1)
import datetime as dt
hadm_mor = {}
miss = 0
miss1 = 0
ddd={}
total = hadm_id_trainlist+hadm_id_vallist+hadm_id_testlist
with open("all_stays.csv","r") as f:
    headers = next(f)
    for line in f:
        line = line.strip().split('"')
        line0 = line[0].split(",")
        if len(line)==3:
            line2 = line[2].split(",")
            line1 = [line[1]]
            line4 = line0[:-1]+line1+line2[1:]
        else:
            line4=line0
        hadmid = line4[1]
        intime = line4[5]
        outtime = line4[6]
        deathtime = line4[10]
        mortality_inh = int(line4[19])
        if mortality_inh == 0:
            hadm_mor[hadmid] = mortality_inh
        else:
            if deathtime == '':
                miss+=1
                dod = line4[15]
                if dod == '':
                    miss1+=1
                    hadm_mor[hadmid] = mortality_inh
                else:
                    #it = datetime.fromisoformat(intime)
                    deathtime = dod
                    intime=intime.replace(' ',',')
                    intime=intime.replace('-',',')
                    intime=intime.replace(':',',')
                    deathtime=deathtime.replace(' ',',')
                    deathtime=deathtime.replace('-',',')
                    deathtime=deathtime.replace(':',',')
                    intime = intime.split(',')
                    deathtime = deathtime.split(',')
                    it = dt.datetime(int(intime[0]),int(intime[1]),int(intime[2]),int(intime[3]),int(intime[4]),int(intime[5]))
                    dtime = dt.datetime(int(deathtime[0]),int(deathtime[1]),int(deathtime[2]),int(deathtime[3]),int(deathtime[4]),int(deathtime[5]))
                    hour=(dtime-it).total_seconds()//3600
                    if hour >96:
                        hadm_mor[hadmid] = 0
                        if hadmid in total:
                            i = hour//24
                            if i not in ddd:
                                ddd[i]=1
                            else:
                                ddd[i]+=1
                    else:
                        hadm_mor[hadmid] = mortality_inh
                        if hadmid in total:
                            i = hour//24
                            if i not in ddd:
                                ddd[i]=1
                            else:
                                ddd[i]+=1
            else:
                intime=intime.replace(' ',',')
                intime=intime.replace('-',',')
                intime=intime.replace(':',',')
                deathtime=deathtime.replace(' ',',')
                deathtime=deathtime.replace('-',',')
                deathtime=deathtime.replace(':',',')
                intime = intime.split(',')
                deathtime = deathtime.split(',')
                it = dt.datetime(int(intime[0]),int(intime[1]),int(intime[2]),int(intime[3]),int(intime[4]),int(intime[5]))
                dtime = dt.datetime(int(deathtime[0]),int(deathtime[1]),int(deathtime[2]),int(deathtime[3]),int(deathtime[4]),int(deathtime[5]))
                
                hour=(dtime-it).total_seconds()//3600
                if hour >96:
                    hadm_mor[hadmid] = 0
                    if hadmid in total:
                        i = hour//24
                        if i not in ddd:
                            ddd[i]=1
                        else:
                            ddd[i]+=1
                else:
                    hadm_mor[hadmid] = mortality_inh
                    if hadmid in total:
                        i = hour//24
                        if i not in ddd:
                            ddd[i]=1
                        else:
                            ddd[i]+=1
#%%
import pickle
import csv

with open("subject_episode_hadm_icu.pickle", "rb") as fp:   # Unpickling
    subject_episode_hadm_icu = pickle.load(fp) 
with open("subject_episode_hadm_icu_test.pickle", "rb") as fp:   # Unpickling
    subject_episode_hadm_icu_test = pickle.load(fp)

#一個list[],存放順序為trainlist的subject_episode幾的順序，存放格式為hadmid。 
hadm_id_trainlist=[]
hadm_id_vallist=[]
hadm_id_testlist=[]
with open("train_listfile.csv",  newline='') as fp:
    rows = csv.reader(fp)
    headers = next(rows)
    for row in rows:
        a=row[0].split('_')[0]#subject
        b=row[0].split('_')[1]#episode
        id1=-1
        for i in subject_episode_hadm_icu[a]:
            if i[0] == b[7:]:
                id1=i[1]#hadm_id
        if id1 ==-1:
            raise ValueError('ValueError')
        hadm_id_trainlist.append(id1)
with open("val_listfile.csv",  newline='') as fp:
    rows = csv.reader(fp)
    headers = next(rows)
    for row in rows:
        a=row[0].split('_')[0]
        b=row[0].split('_')[1]
        id1=-1
        for i in subject_episode_hadm_icu[a]:
            if i[0] == b[7:]:
                id1=i[1]#hadm_id
        if id1 ==-1:
            raise ValueError('ValueError')
        hadm_id_vallist.append(id1)
with open("test_listfile.csv",  newline='') as fp:
    rows = csv.reader(fp)
    headers = next(rows)
    for row in rows:
        a=row[0].split('_')[0]
        b=row[0].split('_')[1]
        id1=-1
        for i in subject_episode_hadm_icu_test[a]:
            if i[0] == b[7:]:
                id1=i[1]#hadm_id
        if id1 ==-1:
            raise ValueError('ValueError')
        hadm_id_testlist.append(id1)
#%%
newlabel_train = []
newlabel_val = []
newlabel_test = []
for i in range(len(hadm_id_trainlist)):
    newlabel_train.append(hadm_mor[hadm_id_trainlist[i]])
for i in range(len(hadm_id_vallist)):
    newlabel_val.append(hadm_mor[hadm_id_vallist[i]])
for i in range(len(hadm_id_testlist)):
    newlabel_test.append(hadm_mor[hadm_id_testlist[i]])

#%%
i_0=0
i_1=0
i_2=0
for i in newlabel_test:
    if i ==1:
        i_1+=1
    elif i ==0:
        i_0+=1
    else:
        i_2+=1
#%%      
with open("./discretization_data/train_data_discretization_v2.pickle", "rb") as fp:
        train_data_discretization = pickle.load(fp)
with open("./discretization_data/val_data_discretization_v2.pickle", "rb") as fp:
        val_data_discretization = pickle.load(fp)
i_0=0
i_1=0
i_2=0      
for i in val_data_discretization[1]:
    if i ==1:
        i_1+=1
    elif i ==0:
        i_0+=1
#%%
with open("newlabel_train.pickle", "wb") as fp:
    pickle.dump(newlabel_train, fp)
with open("newlabel_val.pickle", "wb") as fp:
    pickle.dump(newlabel_val, fp)
with open("newlabel_test.pickle", "wb") as fp:
    pickle.dump(newlabel_test, fp)