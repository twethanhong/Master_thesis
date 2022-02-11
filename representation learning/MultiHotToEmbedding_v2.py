# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:52:49 2020

@author: KDD2070
把所以的值轉成multi-hot的表示方式
轉換成embedding
"""
from sklearn.externals import joblib
import pickle
import numpy as np
import json
mode = 3
# 1:train,2:val,3:test
win = "48"
metapath = "clc"

'''
#LOAD DATA
'''
if mode ==1:
    with open("./discretization_data/discrete_train_data.pickle", "rb") as fp:
        discrete_data = pickle.load(fp)
    with open("./discretization_data/discrete_train_data_newLabel.pickle", "rb") as fp:
        discrete_data_newLabel = pickle.load(fp)
    data_x = discrete_data[0]
    data_y = discrete_data[1]
    data_y_newLabel = discrete_data_newLabel[1]
    '''
    with open("./labevent/train_win"+win+"_"+metapath+"_LabEventEmb.pickle", "rb") as fp:
        lab_emb = pickle.load(fp)
      '''  
elif mode ==2:
    with open("./discretization_data/discrete_val_data.pickle", "rb") as fp:
        discrete_data = pickle.load(fp)
    with open("./discretization_data/discrete_val_data_newLabel.pickle", "rb") as fp:
        discrete_data_newLabel = pickle.load(fp)
    data_x = discrete_data[0]
    data_y = discrete_data[1]
    data_y_newLabel = discrete_data_newLabel[1]
    '''
    with open("./labevent/val_win"+win+"_"+metapath+"_LabEventEmb.pickle", "rb") as fp:
        lab_emb = pickle.load(fp)
        '''
elif mode==3:
    with open("./discretization_data/discrete_test_data.pickle", "rb") as fp:
        discrete_data = pickle.load(fp)
    with open("./discretization_data/discrete_test_data_newLabel.pickle", "rb") as fp:
        discrete_data_newLabel = pickle.load(fp)
    data_x = discrete_data['data'][0]
    data_y = discrete_data['data'][1]
    data_y_newLabel = discrete_data_newLabel['data'][1]
    '''
    with open("./labevent/test_win"+win+"_"+metapath+"_LabEventEmb.pickle", "rb") as fp:
        lab_emb = pickle.load(fp)
        '''

'''
#載入embedding vector
'''
index2nodeid = json.load(open("./Pretrained_Embedding/"+metapath+"/win"+win+"_"+metapath+"_log_win2/index2nodeid.json"))
index2nodeid = {int(k):v for k,v in index2nodeid.items()}
'''
#index:取emb時的編號(矩陣第幾個row)
#nodeid:當初我自己給chartevent,labevent做的編號
'''
nodeid2index = {v:int(k) for k,v in index2nodeid.items()}
node_embeddings = np.load("./Pretrained_Embedding/"+metapath+"/win"+win+"_"+metapath+"_log_win2/node_embeddings.npz")['arr_0']


num2nodeid = {}
with open( "./異構資料/id_chartevent.txt") as f:
    for line in f:
        toks = line.strip().split(" ")
        num2nodeid[toks[1]] = toks[0]
'''
#轉換成embedding的function
'''
def embedding_layer(multihot_list):
    index_list = []
    for i in range(len(multihot_list)):
        if int(multihot_list[i]) == 1:
            index_list.append(i)
    return index_list

def embedding_vector(index_list):
    emb_vec = []
    for i in index_list:
        try:
            node_embeddings[nodeid2index[num2nodeid[str(i)]]]
        except:
            emb_vec.append([0 for i in range(100)])
        else:
            emb_vec.append(node_embeddings[nodeid2index[num2nodeid[str(i)]]])
    return np.array(emb_vec)#emb_vec=17*100
'''
轉換成embedding
'''
data_x_emb = []
data_x_emb_lab = []
er=0
for i in range(len(data_x)):
    array_48_17 =[]
    array_48_18 = []#多加一維是labevent
    for j in range(48):
        embedding_list = embedding_vector(embedding_layer(data_x[i][j]))#embedding_list=17*100
        if len(embedding_list) != 17:
            er+=1
        array_48_17.append(embedding_list)
        '''
        if mode ==1:
            embedding_list = np.append(embedding_list,lab_emb[i][j].reshape(1, 100),axis=0)#embedding_list=18*100
        elif mode ==2:
            embedding_list = np.append(embedding_list,lab_emb[i][j].reshape(1, 100),axis=0)#embedding_list=18*100
        elif mode==3:
            embedding_list = np.append(embedding_list,lab_emb[i][j].reshape(1, 100),axis=0)#embedding_list=18*100
        array_48_18.append(embedding_list)
        '''
    array_48_17 = np.array(array_48_17)
    #array_48_18 = np.array(array_48_18)
    data_x_emb.append(array_48_17)
    #data_x_emb_lab.append(array_48_18)
print('er:',er)

'''
NO LAB
'''

data_x_emb = np.array(data_x_emb)
print(data_x_emb.shape)
data_x_emb =data_x_emb.swapaxes(2,3)
print(data_x_emb.shape)

'''
LAB
'''
'''
data_x_emb_lab = np.array(data_x_emb_lab)
print('data_x_emb_lab.shape',data_x_emb_lab.shape)
data_x_emb_lab =data_x_emb_lab.swapaxes(2,3)
print('data_x_emb_lab.shape',data_x_emb_lab.shape)
'''

data=(data_x_emb,data_y)
data_newlabel=(data_x_emb,data_y_newLabel)
'''
data_lab=(data_x_emb_lab,data_y)
data_lab_newlabel=(data_x_emb_lab,data_y_newLabel)
'''


if mode ==1:
    m="train"
elif mode ==2:
    m="val"
elif mode ==3:
    m="test"
    
    test_data={}
    test_data['data']=data
    test_data['names']=discrete_data['names']
    test_data_newlabel={}
    test_data_newlabel['data']=data_newlabel
    test_data_newlabel['names']=discrete_data['names']
    '''
    test_data_lab={}
    test_data_lab['data']=data_lab
    test_data_lab['names']=discrete_data['names']
    test_data_lab_newlabel={}
    test_data_lab_newlabel['data']=data_lab_newlabel
    test_data_lab_newlabel['names']=discrete_data['names']
    '''

'''
存檔
'''
if mode ==1:
    
    with open("D:/"+m+"_data_win"+win+"_"+metapath+"_2.pickle", "wb") as fp:
        joblib.dump(data, fp,protocol = 4)
    with open("D:/"+m+"_data_win"+win+"_"+metapath+"_newlabel_2.pickle", "wb") as fp:
        joblib.dump(data_newlabel, fp,protocol = 4)
    
    '''
    with open("D:/Emb with LabEvent/"+m+"_data_win"+win+"_"+metapath+"_withlabemb_p1.pickle", "wb") as fp:
        joblib.dump(data_lab, fp)
    
    with open("D:/Emb with LabEvent/"+m+"_data_win"+win+"_"+metapath+"_withlabemb_p2.pickle", "wb") as fp:
        joblib.dump(data_lab_newlabel, fp)
    '''    
elif mode ==2:
    
    with open("D:/"+m+"_data_win"+win+"_"+metapath+"_2.pickle", "wb") as fp:
        joblib.dump(data, fp,protocol = 4)
    with open("D:/"+m+"_data_win"+win+"_"+metapath+"_newlabel_2.pickle", "wb") as fp:
        joblib.dump(data_newlabel, fp,protocol = 4)
    '''
    with open("D:/Emb with LabEvent/"+m+"_data_win"+win+"_"+metapath+"_withlabemb_p1.pickle", "wb") as fp:
        pickle.dump(data_lab, fp,protocol = 4)
    
    with open("D:/Emb with LabEvent/"+m+"_data_win"+win+"_"+metapath+"_withlabemb_p2.pickle", "wb") as fp:
        pickle.dump(data_lab_newlabel, fp,protocol = 4)
      '''  
elif mode ==3:
    
    with open("D:/"+m+"_data_win"+win+"_"+metapath+"_2.pickle", "wb") as fp:
        joblib.dump(test_data, fp,protocol = 4)
    with open("D:/"+m+"_data_win"+win+"_"+metapath+"_newlabel_2.pickle", "wb") as fp:
        joblib.dump(test_data_newlabel, fp,protocol = 4)
    
    '''
    with open("D:/Emb with LabEvent/"+m+"_data_win"+win+"_"+metapath+"_withlabemb_p1.pickle", "wb") as fp:
        pickle.dump(test_data_lab, fp,protocol = 4)
    
    with open("D:/Emb with LabEvent/"+m+"_data_win"+win+"_"+metapath+"_withlabemb_p2.pickle", "wb") as fp:
        pickle.dump(test_data_lab_newlabel, fp,protocol = 4)
     '''   