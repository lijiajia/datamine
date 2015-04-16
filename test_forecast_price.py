#!/usr/bin/env python
# coding=utf-8

import os
from sklearn.svm import NuSVR
from settings import DATA_DIR
from utils import load_data, split_dataset

FILENAME = os.path.join(DATA_DIR, 'boston_house_prices.csv')


if __name__ == '__main__':
    dataset = load_data(FILENAME)
    train_set, test_set = split_dataset(dataset)
    X = [train_data[:-1] for train_data in train_set]
    y = [train_data[-1] for train_data in train_set]
    X_test = [test_data[:-1] for test_data in test_set]
    X_classies = [test_data[-1] for test_data in test_set]

    clf = NuSVR()
    clf.fit(X, y)
    predicts = clf.predict(X_test)
    bias = 0.0
    for (i, predict) in enumerate(predicts):
        bias += abs(predict - X_classies[i])
    print bias / len(X_classies)
