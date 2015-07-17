#!/usr/bin/env python
# coding=utf-8

import os
import csv

ROOT_DIR = '/home/lijiajia/work/datamine/dianping_data'

def process():
    for root, dirs, files in os.walk(ROOT_DIR):
        for filename in files:
            filename_list = filename.split('.')
            filename = filename_list[0]
            print filename, len(filename)
            filename = filename[0:-22]
            print filename
            break
        break

if __name__ == '__main__':
    process()
