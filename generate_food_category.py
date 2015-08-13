#!/usr/bin/env python
# coding=utf-8

import os
import csv
import shutil

ROOT_DIR = '/home/lijiajia/work/datamine/dianping_data'

def process():
    category_set = set()
    shop_set = []
    #city_list = []
    #with open(os.path.join(ROOT_DIR, 'city_list.csv'), 'rb') as f:
    #    reader = csv.reader(f)
    #    for line in reader:
    #        city = line[0]
    #        city_list.append(city)
    #print len(city_list)

    for root, dirs, files in os.walk(ROOT_DIR):
        for filename in files:
            #if not filename.endswith('txt'):
            #    continue
            fn = ROOT_DIR + '/' + filename
            #file = filename[0:-4]
            #file_split = file.split('_')
            #file = file_split[1]
            #if not file in city_list:
            #    shutil.move(fn, '/home/lijiajia/work/datamine/foreign/' + filename)
            #    continue
            with open(fn, 'rb') as f:
                reader_shop = csv.reader(f)
                for line in reader_shop:
                    category = line[0]
                    shop = line[1]
                    category_set |= set([category])
                    shop_set.append(shop)
    for category in list(category_set):
        print category
    print len(list(category_set))
    print len(shop_set)

if __name__ == '__main__':
    process()
