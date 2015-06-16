#!/usr/bin/env python
# coding=utf-8

import sys
import os
import random
from settings import DATA_DIR
import csv

csv.field_size_limit(sys.maxsize)


def process():
    user_ids = set()
    news_ids = set()
    with open(os.path.join(DATA_DIR, 'train_data.txt'), 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            try:
                user_id, news_id = int(line[0]), int(line[1])
                user_ids |= set([user_id])
                news_ids |= set([news_id])
            except:
                pass
    print len(list(user_ids)), len(list(news_ids))
    with open('result_data/predict.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['userid', 'newsid'])
        for user_id in list(user_ids):
            i = random.randint(1, 6182)
            news_id = (list(news_ids))[i]
            writer.writerow([user_id, news_id])


if __name__ == '__main__':
    process()
