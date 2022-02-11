"""
產生一個叫test data 的檔案，是從benckmark的程式中擷取出來的，
已經做完程式中區間化(區間化類別形態特徵，並將連續形態特徵做正規化)，
但還沒做我的區間化(連續形態特徵做區間化)
做我的區間化的檔案在kdd2070電腦中的dataprocess
"""
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import argparse
import os


from mimic3models.in_hospital_mortality import utils
from mimic3benchmark.readers import InHospitalMortalityReader
from mimic3models.preprocessing import Discretizer
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

# Build discretizers, normalizers
train_reader = InHospitalMortalityReader(dataset_dir=os.path.join(args.data, 'train'),
                                         listfile=os.path.join(args.data, 'train_listfile.csv'),
                                         period_length=48.0)
discretizer = Discretizer(timestep=float(args.timestep),
                          store_masks=True,
                          impute_strategy='previous',
                          start_time='zero')
discretizer_header = discretizer.transform(train_reader.read_example(0)["X"])[1].split(',')
del train_reader
cont_channels = [i for (i, x) in enumerate(discretizer_header) if x.find("->") == -1]


test_reader = InHospitalMortalityReader(dataset_dir=os.path.join(args.data, 'test'),
                                            listfile=os.path.join(args.data, 'test_listfile.csv'),
                                            period_length=48.0)
ret = utils.load_data(test_reader, discretizer,args.small_part,
                      return_names=True)
#%%
import pickle
with open("pickle/newlabel_test.pickle", "rb") as fp:   #Pickling
    test_newlabel = pickle.load(fp)
#no_mask
data = ret["data"][0][:,:,0:59]
oldlabel = ret["data"][1]
ret["data"] = (data, oldlabel)
with open("test_data_RawData_Nomask.pickle", "wb") as fp:   #Pickling
    pickle.dump(ret, fp)
    
ret["data"] = (data, test_newlabel)
with open("test_data_RawData_Nomask_newlabel.pickle", "wb") as fp:   #Pickling
    pickle.dump(ret, fp)
del ret

