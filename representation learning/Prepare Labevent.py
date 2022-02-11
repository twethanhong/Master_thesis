# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 21:56:35 2020

@author: KDD2070
建立字典 用hadmid查詢labevent
"""
import csv
import pickle
all_stays= {}#過濾labevent中的病患
with open('all_stays.csv',newline='',encoding='utf-8') as r:
    headers = next(r)
    for line in r:
        line=line.strip()
        line = line.split(',')
        all_stays[line[1]]=line[5]#1:hadm_id,5:intime
#%%
import datetime as dt
labevent = {}
with open('LABEVENTS.csv',newline='',encoding='utf-8') as r:
    headers = next(r)
    for line in r:
        line=line.strip()
        line = line.split(',')
        if line[2] in all_stays:#line[2]='hadm id'
            intime = all_stays[line[2]]#進入ICU時間
            charttime = line[4]#事件發生時間
            intime=intime.replace(' ',',')
            intime=intime.replace('-',',')
            intime=intime.replace(':',',')
            charttime=charttime.replace(' ',',')
            charttime=charttime.replace('-',',')
            charttime=charttime.replace(':',',')
            intime = intime.split(',')
            charttime = charttime.split(',')
            it = dt.datetime(int(intime[0]),int(intime[1]),int(intime[2]),int(intime[3]),int(intime[4]),int(intime[5]))
            ct = dt.datetime(int(charttime[0]),int(charttime[1]),int(charttime[2]),int(charttime[3]),int(charttime[4]),int(charttime[5]))
            if ct>it:
                hour=(ct-it).total_seconds()//3600#計算事件發生時間跟進入icu時間差距
                if hour>48:
                    pass
                else:
                    if line[2] not in labevent:
                        labevent[line[2]]=[]
                        labevent[line[2]].append([hour,line[3],line[8].strip('"')])
                    else:
                        labevent[line[2]].append([hour,line[3],line[8].strip('"')])
#%%                        
with open("prepare_labevent.pickle", "wb") as fp:
    pickle.dump(labevent, fp)
