#!/usr/bin/env python
# coding=utf-8

import os
from settings import DATA_DIR
from utils import load_data, split_dataset
from sklearn.svm import NuSVC

FILENAME = os.path.join(DATA_DIR, 'pima-indians-diabetes.data.csv')


if __name__ == '__main__':
    dataset = load_data(FILENAME)
    train_set, test_set = split_dataset(dataset)
    X = [train_data[:-1] for train_data in train_set]
    y = [int(train_data[-1]) for train_data in train_set]
    X_test = [test_data[:-1] for test_data in test_set]
    X_classies = [int(test_data[-1]) for test_data in test_set]
    svc = NuSVC()
    svc.fit(X, y)
    predicts = svc.predict(X_test)
    correct = 0
    for (i, predict) in enumerate(predicts):
        if predict == X_classies[i]:
            correct += 1
    print correct / (float(len(X_classies))) * 100.0
