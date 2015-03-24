#!/usr/bin/env python
# coding=utf-8

import os
import csv
import time
import math
from settings import DATA_DIR

RATING = {}


def init():
    global RATING
    start_time = int(time.time())
    with open(os.path.join(DATA_DIR, 'movielens_1m/ratings.dat'), 'rb') as f:
        reader = csv.reader(f)
        for line in reader:
            line = line[0].split('::') if line else []
            if line is None or len(line) < 4:
                continue
            user_id, movie_id, rating = line[0], line[1], int(line[2])
            if user_id in RATING:
                RATING[user_id].update({movie_id: rating})
            else:
                RATING.update({user_id: {movie_id: rating}})
    cost_time = int(time.time()) - start_time
    print 'costing time: %d' % cost_time


def sim_pearson(person1, person2):
    global RATING
    sim = {}
    for item in RATING[person1]:
        if item in RATING[person2]:
            sim[item] = 1
    n = len(sim)
    if n == 0:
        return -1

    sum1 = sum([RATING[person1][item] for item in sim])
    sum2 = sum([RATING[person2][item] for item in sim])

    sum1_sq = sum([pow(RATING[person1][item], 2) for item in sim])
    sum2_sq = sum([pow(RATING[person2][item], 2) for item in sim])

    sum_multi = sum([RATING[person1][item] * RATING[person2][item] for item in sim])

    num1 = n * sum_multi - sum1 * sum2
    num2 = math.sqrt((n * sum1_sq - pow(sum1, 2)) * (n * sum2_sq - pow(sum2, 2)))

    if num2 == 0:
        return 0

    return num1 / num2


def top_matches(person, n=20):
    global RATING
    scores = [(sim_pearson(person, other), other) for other in RATING if other != person]
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:n]


def get_recommendations(person, n=5):
    global RATING
    totals = {}
    sim_sums = {}

    for other in RATING:
        if other == person:
            continue
        sim = sim_pearson(person, other)
        if sim <= 0:
            continue
        for item in RATING[other]:
            if item not in RATING[person]:
                totals.setdefault(item, 0)
                totals[item] += RATING[other][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim
    ranks = [(total / sim_sums[item], item) for (item, total) in totals.iteritems()]
    ranks.sort(key=lambda x: x[0], reverse=True)

    return ranks[:n]


def get_average(person):
    global RATING
    sum = 0
    count = 0
    for item in RATING[person]:
        sum += RATING[person][item]
        count += 1
    return sum / count if count != 0 else 3


def get_rating(person, movie, n=20):
    global RATING
    users = top_matches(person, n=n)
    average_of_user = get_average(person)
    sim_sums = 0
    jiaquan_sums = 0
    for sim, other in users:
        average_of_other = get_average(other)
        sim_sums += sim
        jiaquan_sums += (RATING[other][movie] - average_of_other) * sim
    try:
        return average_of_user + jiaquan_sums / sim_sums
    except:
        return average_of_user


if __name__ == '__main__':
    init()
    persons = top_matches('1')
    print persons
    recommendations = get_recommendations('1')
    print recommendations
