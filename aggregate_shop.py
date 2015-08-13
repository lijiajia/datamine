#!/usr/bin/env python
# coding=utf-8

import os
import csv
import json
import re

FILTER_PAT = re.compile(ur'\(.*\)$')

SRC_DIR = '/home/lijiajia/work/datamine/trans_category'
RES_FILE = '/home/lijiajia/work/datamine/shop_filter.txt'

def process():
    shop_map = {}
    for root, dirs, files in os.walk(SRC_DIR):
        for filename in files:
            fn = SRC_DIR + '/' + filename
            with open(fn, 'rb') as f:
                reader = csv.reader(f)
                for line in reader:
                    category = line[0]
                    name = line[1]
                    name = FILTER_PAT.sub('', name)
                    price = int(line[3])
                    kouwei = float(line[5])
                    huanjing = float(line[6])
                    fuwu = float(line[7])

                    if name not in shop_map:
                        shop_map[name] = {
                            'category': category,
                            'count': 1,
                            'price': price,
                            'price_count': 1 if price > 0 else 0,
                            'kouwei': kouwei,
                            'huanjing': huanjing,
                            'fuwu': fuwu,
                            'comment_count': 1 if kouwei > 0.0 else 0,
                        }
                    else:
                        shop_map[name]['count'] += 1
                        shop_map[name]['price'] += price
                        shop_map[name]['price_count'] += (1 if price > 0 else 0)
                        shop_map[name]['kouwei'] += kouwei
                        shop_map[name]['huanjing'] += huanjing
                        shop_map[name]['fuwu'] += fuwu
                        shop_map[name]['comment_count'] += (1 if kouwei > 0.0 else 0)
    with open(RES_FILE, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        for key, value in shop_map.iteritems():
            name = key.strip()
            if name is None or len(name) <= 0:
                continue
            category = value['category']
            count = value['count']
            price_count = value['price_count']
            mean_price = value['price'] // price_count if price_count > 0 else 0
            comment_count = value['comment_count']
            #kouwei = 1.0 * value['kouwei'] / comment_count if comment_count > 0 else 0.0
            #kouwei = '%.1f' % kouwei
            #huanjing = 1.0 * value['huanjing'] / comment_count if comment_count > 0 else 0.0
            #huanjing = '%.1f' % huanjing
            #fuwu = 1.00 * value['fuwu'] / comment_count if comment_count > 0 else 0.0
            #fuwu = '%.1f' % fuwu
            writer.writerow([name, category, mean_price])


if __name__ == '__main__':
    process()
