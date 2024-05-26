import utils
from collections import Counter, defaultdict
import os
from sklearn.model_selection import train_test_split
import numpy as np
import random

def get_class_names_from_ds_dir(ds_dir):
    return sorted(utils.get_subdirs_list(ds_dir))

def get_split_samples_stratified(ds_dir, train_proportion, val_proportion, exts=None, seed=None, extra_logic=None):
    assert train_proportion + val_proportion < 1, 'train_proportion + val_proportion >= 1'
    class_images = utils.get_files_with_ext_in_dir(ds_dir, exts=exts, recursive=False)

    random.seed(seed)
    random.shuffle(class_images)

    test_proportion = 1-train_proportion-val_proportion

    n = len(class_images)
    n_train = max(1, int(train_proportion * n))
    n_val = max(1, int(val_proportion * n))
    n_test = max(1, int(test_proportion * n))

    if extra_logic is not None:
        train, val, test = extra_logic(ds_dir, class_images, class_name, n_train, n_val, n_test)
    else:
        train, val, test = class_images[:n_train], class_images[n_train:n_train+n_val], class_images[n_train+n_val:]
    return train, val, test
    
def make_class_dict(files, class_names):
    # integer representation
    class_dict = {}
    for file in files:
        for i,cl in enumerate(class_names):
            if cl in file:
                class_dict[file] = i
    return class_dict

def get_files_in_dir_counter(class_counter):
    id_num_dict = {}

    for i,cl in enumerate(sorted(class_counter)):
        #print(f'{i} {cl}: {class_counter[cl]} times')
        id_num_dict[i] = class_counter[cl]
    return id_num_dict

def get_items_occuring_less_than_n(class_distribution, n, wav_class_dict):
    undesired_classnames = {key: value for key, value in class_distribution.items() if value < n}
    wav_class_dict_for_splitting = {}
    wav_class_dict_for_appending = {}

    for wav in wav_class_dict.keys():
        if all([undesired_classname not in wav for undesired_classname in undesired_classnames.keys()]):
            wav_class_dict_for_splitting[wav] = wav_class_dict[wav]
        else:
            wav_class_dict_for_appending[wav] = wav_class_dict[wav]
            
    return wav_class_dict_for_splitting, wav_class_dict_for_appending