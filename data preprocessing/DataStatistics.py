# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 23:41:37 2021

@author: YC
統計標準化過後數值的分布
"""

from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import pickle

with open(".pickle", "rb") as fp:
    train_raw = pickle.load(fp)
with open(".pickle", "rb") as fp:
    val_raw = pickle.load(fp)

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

#統計
