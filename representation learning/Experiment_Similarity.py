# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:23:27 2021

@author: KDD204
"""
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
win = "1"
metapath = "clc"
index2nodeid = json.load(open("./Pretrained_Embedding/"+metapath+"/win"+win+"_"+metapath+"_log/index2nodeid.json"))
index2nodeid = {int(k):v for k,v in index2nodeid.items()}
nodeid2index = {v:int(k) for k,v in index2nodeid.items()}
#index:取emb時的編號(矩陣第幾個row)
#nodeid:當初我自己給chartevent,labevent做的編號
node_embeddings = np.load("./Pretrained_Embedding/"+metapath+"/win"+win+"_"+metapath+"_log/node_embeddings.npz")['arr_0']
num2nodeid = {}#chartevent node id
with open( "./異構資料/id_chartevent.txt") as f:
    for line in f:
        toks = line.strip().split(" ")
        num2nodeid[toks[1]] = toks[0]
lab_id = {}
with open( "./異構資料/id_labevent.txt") as f:
    for line in f:
        toks = line.strip().split(" ")
        lab_id[toks[1]] = toks[0]
# node_embeddings[nodeid2index[num2nodeid[str(i)]]]
c_event=[]
l_event=[]
for i,j in index2nodeid.items():
    if j in num2nodeid.values():
        c_event.append(j)
    if j in lab_id.values():
        l_event.append(j)

#%%
chart_name = []
f = open('chart_name.txt')
for line in f.readlines():
    #print(line)
    chart_name.append(line.replace('\n',''))
f.close

#%%
"""
"""
111
"""
c_c = [[0.0 for j in range(len(c_event))]for i in range(len(c_event))]
for i in range(len(c_event)):
    for j in range(len(c_event)):
        similarity=cosine_similarity([node_embeddings[nodeid2index[c_event[i]]]],[node_embeddings[nodeid2index[c_event[j]]]])
        c_c[i][j]=similarity
top10_c_c_num=[0.0 for i in range(10)]
top10_c_c = [(0,0) for i in range(10)]
for i in range(len(c_event)):
    for j in range(i,len(c_event)):
        if i != j:
            if c_c[i][j]>top10_c_c_num[-1]:
                #sort
                if c_c[i][j] >top10_c_c_num[0]:
                    top10_c_c_num.insert(0,c_c[i][j])
                    del top10_c_c_num[-1]
                    top10_c_c.insert(0,(c_event[i],c_event[j]))
                    del top10_c_c[-1]
                else:
                    for k in range(9):
                        if c_c[i][j] < top10_c_c_num[k] and c_c[i][j] > top10_c_c_num[k+1]:
                            top10_c_c_num.insert(k+1,c_c[i][j])
                            del top10_c_c_num[-1]
                            top10_c_c.insert(k+1,(c_event[i],c_event[j]))
                            del top10_c_c[-1]
"""
222
"""
l_l = [[0.0 for j in range(len(l_event))]for i in range(len(l_event))]
for i in range(len(l_event)):
    for j in range(len(l_event)):
        similarity=cosine_similarity([node_embeddings[nodeid2index[l_event[i]]]],[node_embeddings[nodeid2index[l_event[j]]]])
        l_l[i][j]=similarity
top10_l_l_num=[0.0 for i in range(10)]
top10_l_l = [(0,0) for i in range(10)]
for i in range(len(l_event)):
    for j in range(i,len(l_event)):
        if i != j:
            if l_l[i][j]>top10_l_l_num[-1]:
                #sort
                if l_l[i][j] >top10_l_l_num[0]:
                    top10_l_l_num.insert(0,l_l[i][j])
                    del top10_l_l_num[-1]
                    top10_l_l.insert(0,(l_event[i],l_event[j]))
                    del top10_l_l[-1]
                else:
                    for k in range(9):
                        if l_l[i][j] < top10_l_l_num[k] and l_l[i][j] > top10_l_l_num[k+1]:
                            top10_l_l_num.insert(k+1,l_l[i][j])
                            del top10_l_l_num[-1]
                            top10_l_l.insert(k+1,(l_event[i],l_event[j]))
                            del top10_l_l[-1]
"""
333
"""
l_c = [[0.0 for j in range(len(c_event))]for i in range(len(l_event))]

for i in range(len(l_event)):
    for j in range(len(c_event)):
        similarity=cosine_similarity([node_embeddings[nodeid2index[l_event[i]]]],[node_embeddings[nodeid2index[c_event[j]]]])
        l_c[i][j]=similarity
top10_l_c_num=[0.0 for i in range(10)]
top10_l_c = [(0,0) for i in range(10)]
for i in range(len(l_event)):
    for j in range(len(c_event)):
        if l_c[i][j]>top10_l_c_num[-1]:
            #sort
            if l_c[i][j] >top10_l_c_num[0]:
                top10_l_c_num.insert(0,l_c[i][j])
                del top10_l_c_num[-1]
                top10_l_c.insert(0,(l_event[i],c_event[j]))
                del top10_l_c[-1]
            else:
                for k in range(9):
                    if l_c[i][j] < top10_l_c_num[k] and l_c[i][j] > top10_l_c_num[k+1]:
                        top10_l_c_num.insert(k+1,l_c[i][j])
                        del top10_l_c_num[-1]
                        top10_l_c.insert(k+1,(l_event[i],c_event[j]))
                        del top10_l_c[-1]

"""
"""
444
"""
#%%
chart_id = '33' #可以設定
GCS = [str(i) for i in range(22,51)]
Height = [str(i) for i in range(71,81)]
Weight = [str(i) for i in range(131,141)]
chartevent_emb = node_embeddings[nodeid2index[chart_id]]
top10_c_num=[0.0 for i in range(11)]#OUTPUT 最相似的前十名的相似度
top10_c = [0.0 for i in range(11)]#OUTPUT 最相似的前十名
for i in range(len(c_event)):
    if chart_id != c_event[i] and c_event[i] not in GCS and c_event[i] not in Height and c_event[i] not in Weight:
        similarity=cosine_similarity([chartevent_emb],[node_embeddings[nodeid2index[c_event[i]]]])
        if similarity>top10_c_num[-1]:
            #sort
            if similarity>top10_c_num[0]:
                top10_c_num.insert(0,similarity)
                del top10_c_num[-1]
                top10_c.insert(0,c_event[i])
                del top10_c[-1]
            else:
                for k in range(10):
                    if similarity < top10_c_num[k] and similarity > top10_c_num[k+1]:
                        top10_c_num.insert(k+1,similarity)
                        del top10_c_num[-1]
                        top10_c.insert(k+1,c_event[i])
                        del top10_c[-1]
for i in range(11):
    top10_c[i]=chart_name[int(top10_c[i])]
"""
555
Clustering
"""
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering



#data ex

chart_emb=[]
for i in range(len(c_event)):
    chart_emb.append(node_embeddings[nodeid2index[c_event[i]]])
chart_emb = np.array(chart_emb)
n_clusters = 20
'''
KMeans
'''
#cluster  = KMeans(n_clusters=n_clusters,algorithm='auto').fit(chart_emb)
#cluster = SpectralClustering(n_clusters=n_clusters)
'''
Hierarchical Clustering
'''
cluster = AgglomerativeClustering(linkage = 'ward', affinity = 'euclidean', n_clusters = n_clusters).fit(chart_emb)
cluster_labels = cluster.labels_
print("分群結果：")
print(cluster_labels)
print("---")
c_cluster = {}
label2chartname = {}
label_sort = {}
for i in range(len(c_event)):
    if cluster_labels[i] in c_cluster:
        c_cluster[cluster_labels[i]].append(int(c_event[i]))
    else:
        c_cluster[cluster_labels[i]]=[int(c_event[i])]
    #c_cluster[c_event[i]]=cluster_labels[i]

for k in c_cluster:
    c_cluster[k].sort()

for i in range(n_clusters):
    label2chartname[i]=[]
for i in label2chartname:
    for j in c_cluster[i]:
        label2chartname[i].append(chart_name[j])

