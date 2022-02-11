# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 20:13:37 2021

@author: KDD2070
"""
import random
import pickle
winsize = "4"
dirpath = "C://Users//KDD204//Desktop//異構網路嵌入式學習//異構資料//Win="+winsize

outfilename_cpl = "C://Users//KDD204//Desktop//異構網路嵌入式學習//異構資料//Win="+winsize+"//win"+winsize+"_cl.txt"
outfilename_clc = "C://Users//KDD204//Desktop//異構網路嵌入式學習//異構資料//Win="+winsize+"//win"+winsize+"_clc.txt"
outfilename_cpc = "C://Users//KDD204//Desktop//異構網路嵌入式學習//異構資料//Win="+winsize+"//win"+winsize+"_cc.txt"
numwalks = 1000
walklength = 1
'''
generate_random_cpl
'''
with open(dirpath+"/chart_labevent_win"+winsize+".pickle", "rb") as fp:   # Unpickling
    chart_labevent = pickle.load(fp)

outfile = open(outfilename_cpl,'w')
for chart in chart_labevent:
    chart0 =  chart
    for j in range(0,numwalks):
        outline = chart0
        outline = str(outline)
        i=0
        while i<walklength:
            labs = chart_labevent[chart0]
            numl = len(labs)
            labid = random.randrange(numl)
            lab = labs[labid]
            i+=1
            lab = str(lab)
            outline += " "+lab
        outfile.write(outline + "\n")
outfile.close()

'''
generate_random_clc
'''
with open(dirpath+"/chart_labevent_win"+winsize+".pickle", "rb") as fp:   # Unpickling
    chart_labevent = pickle.load(fp)
with open(dirpath+"/lab_chartevent_win"+winsize+".pickle", "rb") as fp:   # Unpickling
    lab_chartevent = pickle.load(fp)

outfile = open(outfilename_clc,'w')
for chart in chart_labevent:
    chart0 =  chart
    for j in range(0,numwalks):
        outline = chart0
        outline = str(outline)
        i=0
        while i<walklength:
            labs = chart_labevent[chart0]
            numl = len(labs)
            labid = random.randrange(numl)
            lab = labs[labid]
            i+=1
            lab = str(lab)
            outline += " "+lab
        i=0    
        while i<walklength:
            charts = lab_chartevent[int(lab)]
            numc = len(charts)
            chartid = random.randrange(numc)
            chart = charts[chartid]
            i+=1
            chart = str(chart)
            outline += " "+chart
        outfile.write(outline + "\n")
outfile.close()

'''
#generate_random_cpc
'''
with open(dirpath+"/chart_chartevent_win"+winsize+".pickle", "rb") as fp:   # Unpickling
    chart_chartevent = pickle.load(fp)

outfile = open(outfilename_cpc,'w')
for chart in chart_chartevent:
    chart0 =  chart
    for j in range(0,numwalks):
        outline = chart0
        outline = str(outline)
        i=0
        while i<walklength:
            charts = chart_chartevent[chart0]
            numc = len(charts)
            chartid = random.randrange(numc)
            chart1 = charts[chartid]
            i+=1
            chart1 = str(chart1)
            outline += " "+chart1
        outfile.write(outline + "\n")
outfile.close()