# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 20:35:42 2021

@author: YC
"""
import numpy as np
import pickle

#original_label
with open("output/test_data_RawData_Nomask.pickle", "rb") as fp:
    train_raw = pickle.load(fp)
'''
#new
with open("output/test_data_RawData_Nomask_newlabel.pickle", "rb") as fp:
    train_raw = pickle.load(fp)
'''    
full_data = train_raw['data'][0]
full_data = full_data.tolist()

#切割區間

'''
2:Diastolic blood pressure
3:#Fraction inspired oxygen
49:#Glucose
50:#Heart rate
51:#Height
52:#Mean blood pressure
53:#Oxygen saturation
54:#Respiratory rate
55:#Systolic blood pressure
56:#Temperature
57:#Weight
58:#pH
'''
cont_channels=[2,3,49,50,51,52,53,54,55,56,57,58]
#range_channels[OUTLIER_LOW,VALID_LOW,VALID_HIGH,OUTLIER_HIGH]
range_channels={2:[0,0,375,375],
                3:[0.2,0.21,1,1.1],
                49:[0,33,2000,2200],
                50:[0,0,350,390],
                51:[0,0,240,275],
                52:[0,14,330,375],
                53:[0,0,100,150],
                54:[0,0,300,330],
                55:[0,0,375,375],
                56:[14.2,26,45,47],
                57:[0,0,250,250],
                58:[6.3,6.3,8.4,10]}

delete_index=[]

for i in range(len(full_data)):
    data = full_data[i]
    for j in cont_channels:
        #處理超過極值(VALID_LOW,VALID_HIGH)但不至於太多的值在(OUTLIER_HIGH,OUTLIER_LOW)之間，歸類在極值。
        for hour in range(48):
            if data[hour][j]>range_channels[j][3]:
                data[hour][j] = np.nan
            elif data[hour][j]<range_channels[j][1]:
                data[hour][j] = np.nan
            elif data[hour][j]>range_channels[j][2]and data[hour][j]<range_channels[j][3]:
                data[hour][j] = range_channels[j][2]
            elif data[hour][j]>range_channels[j][0]and data[hour][j]<range_channels[j][1]:
                data[hour][j] = range_channels[j][1]
        #處理完
        #處理異常值
        for hour in range(48):
            if np.isnan(data[hour][j]):
                #是NAN
                for k in range(hour,48):
                    if np.isnan(data[k][j]):
                        continue
                    else:
                        data[hour][j] = data[k][j]
                        break
                if np.isnan(data[hour][j]):#往下都是NAN
                    if hour == 0:
                        #這筆資料不能用
                        delete_index.append(i)
                        break
                    for k in range(hour-1,-1,-1):#往上找值
                        if np.isnan(data[k][j]):
                            continue
                        else:
                            data[hour][j] = data[k][j]
                            break
            else:
                #不是NAN
                continue
'''
#%%
import csv
#hadm_delete_list 
#讀取Train_liat,val_list(hadm)
with open("pickle/subject_episode_hadm_icu_test.pickle", "rb") as fp:   # Unpickling
    subject_episode_hadm_icu = pickle.load(fp) 

hadm_id_testlist=[]
with open("test_listfile.csv",  newline='') as fp:
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
        hadm_id_testlist.append(id1)
'''
#%%
'''
full_data_hadmid = hadm_id_testlist
'''

#%%
#full_data = train_raw['data'][0]
full_data = np.array(full_data)
full_data = np.delete(full_data,delete_index,0)

full_data_label = np.array(train_raw['data'][1])
full_data_label = np.delete(full_data_label,delete_index)

'''
#異常值hadmid 刪除
full_data_hadmid = np.array(full_data_hadmid)
full_data_hadmid = np.delete(full_data_hadmid,delete_index)
'''
full_data_label = full_data_label.tolist()
full_data_fliename = train_raw['names']
full_data_fliename = np.array(full_data_fliename)
full_data_fliename = np.delete(full_data_fliename,delete_index)
full_data_fliename = full_data_fliename.tolist()
train_raw['names'] = full_data_fliename
#處理完共3222筆
train_raw['data'] = (full_data,full_data_label)
'''
with open("test_data_extract_OUTLIER_newLabel.pickle", "wb") as fp:
    pickle.dump(train_raw, fp)
with open("test_data_extract_OUTLIER_present_with_hadmid.pickle", "wb") as fp:
    pickle.dump(full_data_hadmid, fp)'''
'''
with open("test_data_RawData_Nomask_Remove_OUTLIER.pickle", "wb") as fp:
    pickle.dump(train_raw, fp)'''