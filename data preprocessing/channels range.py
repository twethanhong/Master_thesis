# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 20:29:08 2021

@author: YC
"""
import numpy as np
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

fp = open("channel_ranges.txt", "a")
for key in dict_range:
    fp.write('channel_')
    fp.write(str(key))
    fp.write('\n')
    for v in range(10):
        fp.write(str(round(dict_range[key][v],2)))
        fp.write(' ~ ')
        fp.write(str(round(dict_range[key][v+1],2)))
        fp.write('\n')
fp.close()