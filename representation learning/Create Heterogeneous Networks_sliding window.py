# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 15:51:44 2021

@author: KDD2070
主要輸出4個檔案:
1.id_labevent : 實驗室檢測編碼

2.id_chartevent : 儀器檢測編碼

3.chart_lab_win:

4.chart_chart_win
可以設定window，表示window時間內共同發生的事情都被列為有關連
"""
import pickle
import time

windowsize = 4
winsize = str(windowsize)
'''
存放順序為trainlist,vallist的subject_episode幾的順序，存放格式為hadmid。
'''
with open("input/train_data_extract_OUTLIER_present_with_hadmid.pickle", "rb") as fp:
    hadm_id_trainlist = pickle.load(fp) 
with open("input/val_data_extract_OUTLIER_present_with_hadmid.pickle", "rb") as fp:
    hadm_id_vallist = pickle.load(fp)
'''
#1.編碼-Chart Event
'''
with open("./discretization_data/discrete_train_data.pickle", "rb") as fp:   # Unpickling
    discrete_train_data = pickle.load(fp)
with open("./discretization_data/discrete_val_data.pickle", "rb") as fp:   # Unpickling
    discrete_val_data = pickle.load(fp)

hadmid_chartevent_multi = {}
for i in range(len(hadm_id_trainlist)):
    hadmid_chartevent_multi[hadm_id_trainlist[i]] = discrete_train_data[0][i]
for i in range(len(hadm_id_vallist)):
    hadmid_chartevent_multi[hadm_id_vallist[i]] = discrete_val_data[0][i]

def multi2index(multi_list):
    index_list = []
    for i in range(len(multi_list)):
        if int(multi_list[i]) == 1:
            index_list.append(i)
    return index_list
def array2index(multi_array):
    index_array = []
    for i in multi_array:
        index_array.append(multi2index(i))
    return index_array
hadmid_chartevent = {}
for i in range(len(hadm_id_trainlist)):
    hadmid_chartevent[hadm_id_trainlist[i]] = array2index(discrete_train_data[0][i])
for i in range(len(hadm_id_vallist)):
    hadmid_chartevent[hadm_id_vallist[i]] = array2index(discrete_val_data[0][i])

index_count=151#dict_numdiscre節點數
chartevent2id={}
id2chartevent={}
globalindex = 0
j = 0
for i in range(index_count):
    chartevent2id[i] = j
    id2chartevent[j] = i
    j+=1
globalindex = j
print('globalindex=',globalindex)

'''
2.labevent編碼
'''
labitem=[]
with open('mimic3_資料集/D_LABITEMS.csv',newline='',encoding='utf-8') as r:
    readlines = r.readlines()
    readline = readlines[1:]
    for line in readline:
        line = line.strip().split(',')
        labitem.append(line[1])
lab_id = {}
id_lab = {}
i = globalindex
for item in labitem:
    id_lab[i]= item
    lab_id[item] = i
    i+=1
    item = 'abnormal_'+''.join(item)
    id_lab[i]= item
    lab_id[item] = i
    i+=1
globalindex = i

'''
saving index
'''
'''fp = open("id_chartevent.txt", "a")
for key in id2chartevent:
    fp.write(str(key))
    fp.write(' ')
    fp.write(str(id2chartevent[key]))
    fp.write('\n')
fp.close()
fp = open("id_labevent.txt", "a")
for key,value in id_lab.items():
    fp.write(str(key))
    fp.write(' ')
    fp.write(value)
    fp.write('\n')
fp.close()'''

print("== start ==")
'''
3.Create chart_labevent
'''
with open("prepare_labevent.pickle", "rb") as fp:
    prepare_labevent = pickle.load(fp)
start = time.time()
chart_labevent = {}
win=0
ab=0
pre_lab=0
for hadmid in hadmid_chartevent:
    for i in range(48):
        for j in hadmid_chartevent[hadmid][i]:
            #j chart event index
            if hadmid in prepare_labevent:
                pre_lab+=1
                for k in prepare_labevent[hadmid]:
                    if abs(int(k[0])-i) <= windowsize:
                        win+=1
                        if k[2] == 'abnormal':
                            ab+=1
                            labid = lab_id['abnormal_'+''.join(k[1])]
                        else:
                            labid = lab_id[k[1]]
                        if j not in chart_labevent:
                            chart_labevent[j]=[]
                        chart_labevent[j].append(labid)
    for key,value in chart_labevent.items():
        chart_labevent[key] = list(set(value))
del prepare_labevent
end = time.time()
dtime1 = end - start

for key,value in chart_labevent.items():
    chart_labevent[key] = list(set(value))
print("== chart_labevent is done! ==")    
with open("chart_labevent_win"+winsize+".pickle", "wb") as fp:
    pickle.dump(chart_labevent, fp)
print("== chart_labevent is saved! ==")

'''
4.Create lab_chartevent
'''
lab_chartevent = {}
for k,v in chart_labevent.items():
    for i in v:
        if i in lab_chartevent:
            lab_chartevent[i].append(k)
        else:
            lab_chartevent[i]=[k]
for k in lab_chartevent:
    lab_chartevent[k] = list(set(lab_chartevent[k]))
del chart_labevent
print("== lab_chartevent is done! ==") 
with open("lab_chartevent_win"+winsize+".pickle", "wb") as fp:
    pickle.dump(lab_chartevent, fp)
print("== lab_chartevent is saved! ==")
#%%
del lab_chartevent

'''
5.Create chart_chartevent
'''
start = time.time()
chart_chartevent = {}
m=0
for hadmid in hadmid_chartevent:
    m+=1
    end = time.time()
    dtime2 = end - start
    #print('m:',m)
    for i in range(48):
        #print('i:',i)
        for k in range(48):
            #print('k:',k)
            if abs(k-i) <= windowsize:
                for j in hadmid_chartevent[hadmid][i]:
                    #print('j:',j)
                    for l in hadmid_chartevent[hadmid][k]:
                        #print('l:',l)
                        if j not in chart_chartevent:
                            chart_chartevent[j]=[]
                        chart_chartevent[j].append(l)
    for key,value in chart_chartevent.items():
        chart_chartevent[key] = list(set(value))
end = time.time()                        
dtime3 = end - start

for key,value in chart_chartevent.items():
    chart_chartevent[key] = list(set(value))
print("== chart_chartevent is done! ==") 
with open("chart_chartevent_win"+winsize+".pickle", "wb") as fp:
    pickle.dump(chart_chartevent, fp)
print("== chart_chartevent is saved! ==")
del chart_chartevent

