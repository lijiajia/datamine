#!/usr/bin/env python
# coding=utf-8

import sys
import os
import math
import random
from datetime import datetime
from settings import DATA_DIR
import csv
import matplotlib.pyplot as plt

csv.field_size_limit(sys.maxsize)

interest_dict = {}

def load_interest():
    global interest_dict
    with open(os.path.join(DATA_DIR, 'mfd_day_share_interest.csv'), 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for line in reader:
            date, interest = line[0], float(line[1])
            if date not in interest_dict:
                interest_dict[date] = interest
    #interest_dict = sorted(interest_dict.iteritems(), key=lambda x: x[0])
    #index = []
    #interests = []
    #count = 0
    #for key, value in interest_dict:
    #    count += 1
    #    index.append(count)
    #    interests.append(value)
    #plt.plot(index, interests)
    #plt.savefig('interest.jpg')

def convert_to_week(date):
    time = datetime.strptime(date, '%Y%m%d')
    return time.weekday()

def convert_to_month(date):
    time = datetime.strptime(date, '%Y%m%d')
    return time.monthday()

def process():
    global interest_dict
    y_balance_dict = {}
    purchase_all_dict = {}
    purchase_bal_dict = {}
    purchase_bank_dict = {}
    share_dict = {}
    redeem_all_dict = {}
    tftobal_dict = {}
    tftocard_dict = {}
    consume_dict = {}
    index = []
    with open(os.path.join(DATA_DIR, 'user_balance_table.csv'), 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for line in reader:
            date = line[1]
            if date < '20140601':
                continue
            y_balance = int(line[3])
            purchase_all_amt = int(line[4])
            purchase_bal_amt = int(line[6])
            purchase_bank_amt = int(line[7])
            share_amt = int(line[13])
            redeem_all_amt = int(line[8])
            tftobal_amt = int(line[11])
            tftocard_amt = int(line[12])
            consume_amt = int(line[9])
            category_1 = int(line[14]) if consume_amt > 0 else 0
            category_2 = int(line[15]) if consume_amt > 0 else 0
            category_3 = int(line[16]) if consume_amt > 0 else 0
            category_4 = int(line[17]) if consume_amt > 0 else 0

            if date not in y_balance_dict:
                y_balance_dict[date] = y_balance
                purchase_all_dict[date] = purchase_all_amt
                purchase_bal_dict[date] = purchase_bal_amt
                purchase_bank_dict[date] = purchase_bank_amt
                share_dict[date] = share_amt
                redeem_all_dict[date] = redeem_all_amt
                tftobal_dict[date] = tftobal_amt
                tftocard_dict[date] = tftocard_amt
                consume_dict[date] = consume_amt
            else:
                y_balance_dict[date] += y_balance
                purchase_all_dict[date] += purchase_all_amt
                purchase_bal_dict[date] += purchase_bal_amt
                purchase_bank_dict[date] += purchase_bank_amt
                share_dict[date] += share_amt
                redeem_all_dict[date] += redeem_all_amt
                tftobal_dict[date] += tftobal_amt
                tftocard_dict[date] += tftocard_amt
                consume_dict[date] += consume_amt

    y_balance_list = []
    for (key, value) in sorted(y_balance_dict.iteritems(), key=lambda x: x[0]):
        y_balance_list.append(value)

    purchase_all_list = []
    purchase_all = [0, 0, 0, 0, 0, 0, 0]
    count = [0, 0, 0, 0, 0, 0, 0]
    purchase_mean = [0, 0, 0, 0, 0, 0, 0]
    for (key, value) in sorted(purchase_all_dict.iteritems(), key=lambda x: x[0]):
        i = convert_to_week(key)
        purchase_all[i] += value
        count[i] += 1
        purchase_all_list.append(math.log10(value))
    for i in xrange(0, 7):
        purchase_mean[i] = purchase_all[i] / count[i]

    purchase_bal_list = []
    for (key, value) in sorted(purchase_bal_dict.iteritems(), key=lambda x: x[0]):
        purchase_bal_list.append(value)

    purchase_bank_list = []
    for (key, value) in sorted(purchase_bank_dict.iteritems(), key=lambda x: x[0]):
        purchase_bank_list.append(value)

    redeem_all_list = []
    redeem_all = [0, 0, 0, 0, 0, 0, 0]
    count = [0, 0, 0, 0, 0, 0, 0]
    redeem_mean = [0, 0, 0, 0, 0, 0, 0]
    for (key, value) in sorted(redeem_all_dict.iteritems(), key=lambda x: x[0]):
        i = convert_to_week(key)
        redeem_all[i] += value
        count[i] += 1
        redeem_all_list.append(math.log10(value))
    for i in xrange(0, 7):
        redeem_mean[i] = redeem_all[i] / count[i]

    for i in xrange(len(purchase_all_list)):
        index.append(i+1)
    plt.plot(index, purchase_all_list)
    plt.plot(index, redeem_all_list)
    #plt.plot(index, y_balance_list)
    #plt.plot(index, purchase_bal_list)
    #plt.plot(index, purchase_bank_list)
    plt.savefig('res.jpg')

    index = []
    purchase_predict = []
    redeem_predict = []
    with open('tc_comp_predict_table.csv', 'wb') as f:
        writer = csv.writer(f)
        for date in xrange(20140901, 20140931):
            i = convert_to_week(str(date))
            purchase_predict.append(purchase_mean[i])
            redeem_predict.append(redeem_mean[i])
            writer.writerow([str(date), purchase_mean[i], redeem_mean[i]])

if __name__ == '__main__':
    load_interest()
    process()
