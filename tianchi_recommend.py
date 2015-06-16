#!/usr/bin/env python
# coding=utf-8

import os
import csv
from settings import DATA_DIR

FILE_DIR = os.path.join(DATA_DIR, 'tianchi_mobile_recommend_train_user.csv')


def load_data():
    with open(FILE_DIR, 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        n = 0
        for line in reader:
            print line
            n += 1
        print n


if __name__ == '__main__':
    load_data()

