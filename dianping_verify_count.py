#!/usr/bin/env python
# coding=utf-8

import os
import csv
import requests
import random
import time
from BeautifulSoup import BeautifulSoup
from env import USER_AGENT_CHOICES

HOST = 'http://www.dianping.com'
SRC_DIR = '/home/lijiajia/work/datamine/dianping_data'
URL = 'http://www.dianping.com/search/category/%d/10'

def process():
    headers = {'Referer': HOST}
    headers['User-Agent'] = random.choice(USER_AGENT_CHOICES)
    for root, dirs, files in os.walk(SRC_DIR):
        for filename in files:
            fn = SRC_DIR + '/' + filename
            num = int((filename.split('_'))[0])
            url = URL % num
            r = requests.get(url, headers=headers, verify=False)
            time.sleep(0.5)
            if r.status_code != 200:
                print url, r.status_code
                continue
            real_count = 0
            soup = BeautifulSoup(r.content)
            num_tag = soup.find('span', {'class': 'num'})
            try:
                num_tag = num_tag.text
                num_tag = num_tag[1:-1]
                real_count = int(num_tag)
            except:
                continue
            
            with open(fn, 'rb') as f:
                reader = csv.reader(f)
                count = 0
                for line in reader:
                    count += 1
            if real_count > 0 and 1.0 * count / real_count < 0.95:
                print 'not satisfied', num
            else:
                print count


if __name__ == '__main__':
    process()
