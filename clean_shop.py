#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import re

ENG_BRACKET_PAT = re.compile('\(.*\)')
CHI_BRACKET_PAT = re.compile('（.*）')

FILTER_FILE = '/home/lijiajia/work/datamine/filter_out.txt'
SRC_FILE = '/home/lijiajia/work/datamine/restaurants.txt'
DST_FILE = '/home/lijiajia/work/datamine/restaurants_strict.txt'

def process():
    shop_list = []
    filter_list = []
    with open(FILTER_FILE, 'rb') as f:
        reader = csv.reader(f)
        for line in reader:
            filter_list.append((line[0])[1:])
    with open(SRC_FILE, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            shop = line[0]
            shop = ENG_BRACKET_PAT.sub('', shop)
            shop = CHI_BRACKET_PAT.sub('', shop)
            if len(shop) > 0 and not shop.isdigit() and '超值' not in shop and '单人' not in shop and '双人' not in shop and '通用' not in shop:
                shop_list.append([shop, line[1], line[2]])
    with open(DST_FILE, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        for shop in shop_list:
            writer.writerow(shop)


if __name__ == '__main__':
    process()
