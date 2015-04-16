#!/usr/bin/env python
# coding=utf-8

import csv
import random


def load_data(filename):
    dataset = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for line in reader:
            try:
                dataset.append([float(_) for _ in line])
            except Exception as e:
                print 'data format error: %s' % str(e)
                continue
    return dataset


def split_dataset(dataset, split_ratio=0.8):
    train_size = int(len(dataset) * split_ratio)
    train_set = []
    test_set = dataset
    for i in xrange(train_size):
        index = random.randrange(len(test_set))
        train_set.append(test_set.pop(index))
    return train_set, test_set
