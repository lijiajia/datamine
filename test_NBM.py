#!/usr/bin/env python
# coding=utf-8

import os
import csv
import random
import math
from settings import DATA_DIR

FILENAME = os.path.join(DATA_DIR, 'pima-indians-diabetes.data.csv')
#FILENAME = os.path.join(DATA_DIR, 'iris.csv')


def load_csv(filename):
    dataset = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for line in reader:
            dataset.append([float(_) for _ in line])
    return dataset


def split_dataset(dataset, split_ratio=0.8):
    train_size = int(len(dataset) * split_ratio)
    train_set = []
    test_set = dataset
    for i in xrange(train_size):
        index = random.randrange(len(test_set))
        train_set.append(test_set.pop(index))
    return train_set, test_set


def separate_by_class(dataset):
    separated = {}
    for vector in dataset:
        if vector[-1] not in separated:
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries


def summarize_by_class(dataset):
    separated = separate_by_class(dataset)
    summaries = {}
    for class_value, instances in separated.iteritems():
        summaries[class_value] = summarize(instances)
    return summaries


def calculate_probability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent


def calculate_class_probabilities(summaries, input_vector):
    probabilities = {}
    for class_value, class_summaries in summaries.iteritems():
        probabilities[class_value] = 1
        for i in xrange(len(class_summaries)):
            mean, stdev = class_summaries[i]
            x = input_vector[i]
            probabilities[class_value] *= calculate_probability(x, mean, stdev)
    return probabilities


def predict(summaries, input_vector):
    probabilities = calculate_class_probabilities(summaries, input_vector)
    best_label, bestprop = None, -1
    for class_value, probability in probabilities.iteritems():
        if best_label is None or probability > bestprop:
            bestprop = probability
            best_label = class_value
    return best_label


def get_predictions(summaries, test_set):
    predictions = []
    for data in test_set:
        result = predict(summaries, data)
        predictions.append(result)
    return predictions


def get_accuracy(test_set, predictions):
    correct = 0
    for i in xrange(len(test_set)):
        if test_set[i][-1] == predictions[i]:
            correct += 1
    return (correct / float(len(test_set))) * 100.0


dataset = load_csv(FILENAME)
train_set, test_set = split_dataset(dataset, 0.7)
summaries = summarize_by_class(train_set)
predictions = get_predictions(summaries, test_set)
probability = get_accuracy(test_set, predictions)
print probability
