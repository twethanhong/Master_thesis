# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:06:11 2021

@author: KDD204
"""

import pickle
import numpy as np
import json

win = "4"
metapath = "cc"
lab_id = {}
with open( "./異構資料/id_labevent.txt") as f:
    for line in f:
        toks = line.strip().split(" ")
        lab_id[toks[1]] = toks[0]

with open("prepare_labevent.pickle", "rb") as fp:
    prepare_labevent = pickle.load(fp)
labevent_v2={}
for hadm in prepare_labevent:
    labevent_v2[hadm]=[[]for i in range(48)]
    for j in prepare_labevent[hadm]:
        hour = int(j[0])
        if hour<48:
            if j[2]=='abnormal':
                labid = lab_id['abnormal_'+''.join(j[1])]
            else:
                labid = lab_id[j[1]]
            labevent_v2[hadm][hour].append(labid)


#%%
#一個list[],存放順序為trainlist的subject_episode幾的順序，存放格式為hadmid。 
with open("./input/train_data_extract_OUTLIER_present_with_hadmid.pickle", "rb") as fp:
    hadm_id_trainlist = pickle.load(fp)
with open("./input/val_data_extract_OUTLIER_present_with_hadmid.pickle", "rb") as fp:
    hadm_id_vallist = pickle.load(fp)
with open("./input/test_data_extract_OUTLIER_present_with_hadmid.pickle", "rb") as fp:
    hadm_id_testlist = pickle.load(fp)
#%%
index2nodeid = json.load(open("./Pretrained_Embedding/"+metapath+"/win"+win+"_"+metapath+"_log/index2nodeid.json"))
index2nodeid = {int(k):v for k,v in index2nodeid.items()}
nodeid2index = {v:int(k) for k,v in index2nodeid.items()}
#index:取emb時的編號(矩陣第幾個row)
#nodeid:當初我自己給chartevent,labevent做的編號
node_embeddings = np.load("./Pretrained_Embedding/"+metapath+"/win"+win+"_"+metapath+"_log/node_embeddings.npz")['arr_0']        
#%%
def embedding_vector(node_id_list):
    if len(node_id_list)==0:
        return np.array([0.0 for i in range(100)])
    emb_vec = []
    for i in node_id_list:
        try:
            nodeid2index[str(i)]
        except:
            emb_vec.append(np.array([0.0 for i in range(100)],dtype=float))
        else:
            emb_vec.append(node_embeddings[nodeid2index[str(i)]])
    fi_emb=[]
    for j in range(100):
        max_=-100000
        for i in emb_vec:
            if i[j]>max_:
                max_=i[j]
        fi_emb.append(max_)
    return np.array(fi_emb)
error=0
train_lab_emb=[]
for hadm in hadm_id_trainlist:
    hour_list=[]
    try:
        labevent_v2[hadm]
        
    except:
        error+=1
        for hour in range(48):
            hour_list.append(embedding_vector([]))
    else:
        for hour in labevent_v2[hadm]:
            hour_list.append(embedding_vector(hour))
    train_lab_emb.append(hour_list)
val_lab_emb=[]
for hadm in hadm_id_vallist:
    hour_list=[]
    try:
        labevent_v2[hadm]
    except:
        error+=1
        for hour in range(48):
            hour_list.append(embedding_vector([]))
    else:
        for hour in labevent_v2[hadm]:
            hour_list.append(embedding_vector(hour))
    val_lab_emb.append(hour_list)
test_lab_emb=[]
for hadm in hadm_id_testlist:
    hour_list=[]
    try:
        labevent_v2[hadm]
    except:
        error+=1
        for hour in range(48):
            hour_list.append(embedding_vector([]))
    else:
        for hour in labevent_v2[hadm]:
            hour_list.append(embedding_vector(hour))
    test_lab_emb.append(hour_list)
#%%
with open("./labevent/train_win"+win+"_"+metapath+"_LabEventEmb.pickle", "wb") as fp:
    pickle.dump(train_lab_emb, fp)
with open("./labevent/val_win"+win+"_"+metapath+"_LabEventEmb.pickle", "wb") as fp:
    pickle.dump(val_lab_emb, fp)
with open("./labevent/test_win"+win+"_"+metapath+"_LabEventEmb.pickle", "wb") as fp:
    pickle.dump(test_lab_emb, fp)