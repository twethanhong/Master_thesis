# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 16:08:15 2021

@author: YC
原始檔案
尚未除去極端異常值

"""

from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import argparse
import os

from mimic3models.in_hospital_mortality import utils
from mimic3benchmark.readers import InHospitalMortalityReader
from mimic3models.preprocessing import Discretizer, Normalizer
from mimic3models import common_utils

parser = argparse.ArgumentParser()
common_utils.add_common_arguments(parser)
parser.add_argument('--target_repl_coef', type=float, default=0.0)
parser.add_argument('--data', type=str, help='Path to the data of in-hospital mortality task',
                    default='data/in-hospital-mortality/')
parser.add_argument('--output_dir', type=str, help='Directory relative which all output files are stored',
                    default='.')
args = parser.parse_args()
print(args)

if args.small_part:
    args.save_every = 2**30

#parameter
data = 'data/in-hospital-mortality/'
timestep = 1.0

# Build readers, discretizers, normalizers

train_reader = InHospitalMortalityReader(dataset_dir=os.path.join(data, 'train'),
                                         listfile=os.path.join(data, 'train_listfile.csv'),
                                         period_length=48.0)

#train_reader_example = train_reader.read_example(0)["X"]

val_reader = InHospitalMortalityReader(dataset_dir=os.path.join(data, 'train'),
                                       listfile=os.path.join(data, 'val_listfile.csv'),
                                       period_length=48.0)

discretizer = Discretizer(timestep=float(timestep),
                          store_masks=True,
                          impute_strategy='previous',
                          start_time='zero')
#離散過後
discretizer_example = discretizer.transform(train_reader.read_example(0)["X"])[0]

discretizer_header = discretizer.transform(train_reader.read_example(0)["X"])[1].split(',')

discretizer_header = discretizer_header[0:59]

cont_channels = [i for (i, x) in enumerate(discretizer_header) if x.find("->") == -1]
print('discret is done!')

#%%
normalizer = Normalizer(fields=cont_channels)  
# choose here which columns to standardize
normalizer_state = args.normalizer_state

if normalizer_state is None:
    normalizer_state = 'ihm_ts{}.input_str_{}.start_time_zero.normalizer'.format(args.timestep, args.imputation)
    normalizer_state = os.path.join('C://Users//YC//Desktop//dataprocess_v1//mimic3models//in_hospital_mortality', normalizer_state)
normalizer.load_params(normalizer_state)

args_dict = dict(args._get_kwargs())
args_dict['header'] = discretizer_header
args_dict['task'] = 'ihm'
print('normalizer is done!')

#%%
# Read data
train_raw = utils.load_data(train_reader, discretizer)
train_raw_x=train_raw[0][:,:,0:59]
train_raw_y=train_raw[1]

val_raw = utils.load_data(val_reader, discretizer)
val_raw_x=val_raw[0][:,:,0:59]
val_raw_y=val_raw[1]

train_raw_noMask = (train_raw_x,train_raw_y)
val_raw_noMask = (val_raw_x,val_raw_y)
print('Reading data!')

#輸出成檔案
import pickle
with open("train_data_RawData_Nomask.pickle", "wb") as fp:   #Pickling
    pickle.dump(train_raw_noMask, fp)
with open("val_data_RawData_Nomask.pickle", "wb") as fp:   #Pickling
    pickle.dump(val_raw_noMask, fp)
#%%

#讀取NewLabel的檔案
with open("pickle/newlabel_train.pickle", "rb") as fp:   #Pickling
    train_newlabel = pickle.load(fp)
with open("pickle/newlabel_val.pickle", "rb") as fp:   #Pickling
    val_newlabel = pickle.load(fp)

#製做no mask給benchmark model訓練作為basle line
train_raw_noMask_newlabel = (train_raw_x,train_newlabel)
val_raw_noMask_newlabel = (val_raw_x,val_newlabel)

#輸出檔案
with open("train_data_RawData_Nomask_newlabel.pickle", "wb") as fp:
    pickle.dump(train_raw_noMask_newlabel, fp)
with open("val_data_RawData_Nomask_newlabel.pickle", "wb") as fp:
    pickle.dump(val_raw_noMask_newlabel, fp)
    
#輸出檔案:
#train_data_RawData_Nomask,
#val_data_RawData_Nomask,
#train_data_RawData_Nomask_newlabel,val_data_RawData_Nomask_newlabel