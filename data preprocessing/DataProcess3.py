# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 21:57:44 2021

@author: YC

區間化

"""
import numpy as np
import pickle

#old_label
with open("output/train_data_extract_OUTLIER.pickle", "rb") as fp:
    train_data = pickle.load(fp)
with open("output/val_data_extract_OUTLIER.pickle", "rb") as fp:
    val_data = pickle.load(fp)
    
'''
#new_label
with open("output/train_data_extract_OUTLIER_newlabel.pickle", "rb") as fp:
    train_data = pickle.load(fp)
with open("output/val_data_extract_OUTLIER_newlabel.pickle", "rb") as fp:
    val_data = pickle.load(fp)    
'''
'''
import json
with open("mimic3models/resources/channel_info.json") as channel_info_file:
        channel_info = json.loads(channel_info_file.read())
#channel_info's type is dict
'''

cont_channels=[2,3,49,50,51,52,53,54,55,56,57,58]#共12個
range_channels_max_min = {2:[0,375],
                3:[0.21,1],
                49:[33,2000],
                50:[0,350],
                51:[0,240],
                52:[14,330],
                53:[0,100],
                54:[0,300],
                55:[0,375],
                56:[26,45],
                57:[0,250],
                58:[6.3,8.4]}
dict_range = {}
for i in range_channels_max_min:
    dict_range[i]=np.linspace(range_channels_max_min[i][0],range_channels_max_min[i][1],11)


train_data_x = train_data[0]
train_data_y = train_data[1]
val_data_x = val_data[0]
val_data_y = val_data[1]

T=[0,0]
for i in train_data_y:
    if i ==1:
        T[1]+=1
    else:
        T[0]+=1
V=[0,0]
for i in val_data_y:
    if i ==1:
        V[1]+=1
    else:
        V[0]+=1
#%%
def trans(raw_num,k):
    if raw_num<=dict_range[k][0]:
        return 0
    elif raw_num>=dict_range[k][10]:
        return 9
    else:
        for i in range(0,10):
            if raw_num>=dict_range[k][i] and raw_num<dict_range[k][i+1]:
                return i
#%%
GCS1 = [i for i in range(4,12)]
GCS2 = [i for i in range(12,24)]
GCS3 = [i for i in range(24,37)]
GCS4 = [i for i in range(37,49)]

GCS_dict = {4:2,5:3,6:1,7:4,8:0,9:3,10:4
            ,11:2,12:0,13:2,14:1,15:0,16:3,17:4,18:3,19:5,20:2
            ,21:5,22:4,23:1,24:8,25:7,26:10,27:9,28:12,29:11,30:0
            ,31:2,32:1,33:4,34:3,35:6,36:5,37:0,38:0,39:3,40:2
            ,41:4,42:0,43:4,44:1,45:0,46:3,47:1,48:2}

def trans_to_discrete(data_x):
    data_x_discrete = []
    for i in range(len(data_x)):#i是進入ICU的index
        data = []
        for j in range(48):#48小時
            v = []
            for k in range(59):
                if k in cont_channels:
                    #落在哪一個區間
                    a = trans(data_x[i][j][k],k)
                    b = [0 for i in range(10)]
                    b[a] = 1
                    v = v+b
                    del(a)
                    del(b)
                elif k in GCS1:
                    if data_x[i][j][k] ==1:
                        c=[0 for i in range(5)]
                        c[GCS_dict[k]] = 1
                        v = v+c
                        del(c)
                elif k in GCS2:
                    if data_x[i][j][k] ==1:
                        c=[0 for i in range(6)]
                        c[GCS_dict[k]] = 1
                        v = v+c
                        del(c)
                elif k in GCS3:
                    if data_x[i][j][k] ==1:
                        c=[0 for i in range(13)]
                        c[GCS_dict[k]] = 1
                        v = v+c
                        del(c)
                elif k in GCS4:    
                    if data_x[i][j][k] ==1:
                        c=[0 for i in range(5)]
                        c[GCS_dict[k]] = 1
                        v = v+c
                        del(c)
                else:
                    v.append(data_x[i][j][k])
            data.append(v)
            del(v)
        data_x_discrete.append(data)
        del(data)
    return data_x_discrete


train_x_discrete = trans_to_discrete(train_data_x)
'''
train_x_discrete = np.array(train_x_discrete)
val_x_discrete = trans_to_discrete(val_data_x)
val_x_discrete = np.array(val_x_discrete)
# 刪除重複+分隔區間化後共151個節點
#合併
train_data = (train_x_discrete,train_data_y)
val_data = (val_x_discrete,val_data_y)
#%%
#處理完極端值，存檔
import pickle
with open("discrete_train_data_V2.pickle", "wb") as fp:   #Pickling
    pickle.dump(train_data, fp)
with open("discrete_val_data_V2.pickle", "wb") as fp:   #Pickling
    pickle.dump(val_data, fp)'''