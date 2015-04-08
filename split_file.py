#!/usr/bin/env python
# coding=utf-8

import os
from settings import DATA_DIR
import csv
import time


def process():
    start_time = int(time.time())
    i = 0
    with open(os.path.join(DATA_DIR, 'train_data.txt'), 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for i, line in enumerate(reader):
            i += 1
            file_name = '%s.txt' % str(i + 1)
            with open(os.path.join(os.path.dirname(__file__), file_name), 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(line)
            if i >= 1000:
                break

    cost_time = int(time.time()) - start_time
    print 'cost time %d(s)' % cost_time


if __name__ == '__main__':
    process()
