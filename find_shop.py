#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv

SRC_FILE = '/home/lijiajia/work/datamine/restaurants.txt'

def main(argv=sys.argv):
    shop_name = argv[1]
    big = 0
    small = 1000
    count = 0
    with open(SRC_FILE, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            count += 1
            if shop_name in line[0] and line[0] in shop_name:
                print line[0], line[1], line[2], count
            #if len(line[0]) > big:
            #    big = len(line[0])
            #    big_name = line[0]
            #if len(line[0]) > 35:
            #    count += 1
            #if len(line[0]) < small:
            #    small = len(line[0])
            #    small_name = line[0]
            #    small_category = line[1]
            #    small_price = line[2]
            #if line[0].isdigit():
            #    print line[0], line[1], line[2]
        #print big, big_name
        #print small, small_name, small_category, small_price
        #print count

if __name__ == '__main__':
    main()
