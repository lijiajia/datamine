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


def top_matches(person, movie=None, top_n=None):
    global RATING
    if movie is None:
        rating_list = [_ for _ in RATING]
    else:
        rating_list = [_ for _ in RATING if movie in RATING[_]]
    scores = [(sim_pearson(person, other), other) for other in rating_list if other != person]
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores if top_n is None else scores[:top_n]


def get_average(person):
    global RATING
    count = 0
    sum = 0.0
    for item in RATING[person]:
        sum += RATING[person][item]
        count += 1
    # return sum / count
    return 0


def get_recommendations(person, top_n=5):
    global RATING
    sim_sums = {}
    jiaquan_sums = {}

    average_user = get_average(person)
    for other in RATING:
        if other == person:
            continue
        sim = sim_pearson(person, other)
        if sim == 0:
            continue
        sim = abs(sim)
        average_other = get_average(other)
        for item in RATING[other]:
            if item not in RATING[person]:
                jiaquan_sums.setdefault(item, 0)
                jiaquan_sums[item] += (RATING[other][item] - average_other) * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim
    ranks = [(average_user + jiaquan / sim_sums[item], item) for (item, jiaquan) in jiaquan_sums.iteritems()]
    ranks.sort(key=lambda x: x[0], reverse=True)

    return ranks[:top_n]


def get_rating(person, movie, top_n=None):
    global RATING
    users = top_matches(person, movie=movie, top_n=top_n)
    average_user = get_average(person)
    sim_sums = 0.0
    jiaquan_sums = 0.0
    for sim, other in users:
        if sim == 0:
            continue
        average_other = get_average(other)
        sim = abs(sim)
        sim_sums += sim
        jiaquan_sums += (RATING[other][movie] - average_other) * sim
    return average_user + jiaquan_sums / sim_sums if sim_sums > 0 else average_user


if __name__ == '__main__':
    init()
    persons = top_matches('1', top_n=10)
    print persons
    recommendations = get_recommendations('2')
    print recommendations
    print get_rating('1', '3382')
