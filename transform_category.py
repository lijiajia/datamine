#!/usr/bin/env python
# coding=utf-8

import os
import csv
import json

CATEGORY_FILE = '/home/lijiajia/work/datamine/category_map.txt'
SRC_DIR = '/home/lijiajia/work/datamine/dianping_data'
DST_DIR = '/home/lijiajia/work/datamine/trans_category'

def process():
    category_map = {}
    with open(CATEGORY_FILE, 'rb') as f:
        reader = csv.reader(f)
        for line in reader:
            category = line[0]
            res = line[1]
            category_map[category] = res
    print json.dumps(category_map, ensure_ascii=False)

    for root, dirs, files in os.walk(SRC_DIR):
        for filename in files:
            fn = SRC_DIR + '/' + filename
            with open(fn, 'rb') as f:
                reader = csv.reader(f)
                with open(os.path.join(DST_DIR, filename), 'wb') as f1:
                    writer = csv.writer(f1)
                    for line in reader:
                        category = line[0]
                        res_category = category_map.get(category, category)
                        try:
                            writer.writerow([res_category, line[1], line[2], line[3], line[4], line[5], line[6], line[7]])
                        except Exception as e:
                            print json.dumps(line, ensure_ascii=False), str(e), filename


if __name__ == '__main__':
    process()
