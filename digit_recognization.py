#!/usr/bin/env python
# coding=utf-8

import os
import csv
from settings import DATA_DIR
from sklearn.linear_model import LogisticRegression

TRAIN_FILE = os.path.join(DATA_DIR, 'train.csv')
TEST_FILE = os.path.join(DATA_DIR, 'test.csv')


def load_data(filename):
    data_set = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for line in reader:
            data_set.append(line)
    return data_set


def process():
    train_set = load_data(TRAIN_FILE)
    test_set = load_data(TEST_FILE)

    X = [_[1:] for _ in train_set]
    y = [_[0] for _ in train_set]

    clf = LogisticRegression()
    clf.fit(X, y)
    predicts = clf.predict(test_set)

    with open('res.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['ImageId', 'Label'])
        for i, _ in enumerate(predicts):
            writer.writerow([i + 1, _])


if __name__ == '__main__':
    process()
