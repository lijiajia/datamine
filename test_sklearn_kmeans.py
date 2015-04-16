#!/usr/bin/env python
# coding=utf-8

import os
from settings import DATA_DIR
from utils import load_data, split_dataset
from sklearn.cluster import KMeans

FILENAME = os.path.join(DATA_DIR, 'pima-indians-diabetes.data.csv')


if __name__ == '__main__':
    dataset = load_data(FILENAME)
    train_set, test_set = split_dataset(dataset)
    X = [train_data[:-1] for train_data in train_set]
    y = [int(train_data[-1]) for train_data in train_set]
    X_test = [test_data[:-1] for test_data in test_set]
    X_classies = [test_data[-1] for test_data in test_set]

    clf = KMeans(n_clusters=3)
    clf.fit(X)
    predicts = clf.predict(X_test)
    print predicts
    correct = 0
    for (i, predict) in enumerate(predicts):
        if predict == X_classies[i]:
            correct += 1
    print correct / float(len(X_classies)) * 100.0
