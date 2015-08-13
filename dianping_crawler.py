#!/usr/bin/env python
# coding=utf-8

# format: category name fullname price addr kouwei huanjing fuwu

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import requests
import random
import csv
import re
import time
from multiprocessing import Pool
from settings import BASE_DIR
from BeautifulSoup import BeautifulSoup
from env import USER_AGENT_CHOICES 

HOST = 'http://www.dianping.com'
FOOD_URL = 'http://www.dianping.com/search/category/%d/10'
CITY_URL = 'http://www.dianping.com/citylist'
DIAN_PING_DIR = os.path.join(BASE_DIR, 'dianping_data')

PAT = re.compile(ur'[\(\（].+店[\)\）]')


def fetch(url, category_name):
    headers = {'Referer': HOST}
    headers['User-Agent'] = random.choice(USER_AGENT_CHOICES)
    ret = []
    r = requests.get(url, headers=headers, verify=False)
    time.sleep(0.5)
    if r.status_code != 200:
        print url, r.status_code
        return
    soup = BeautifulSoup(r.content)
    try:
        shop_list = soup.find('div', {'id': 'shop-all-list'}).findAll('li')
        for shop in shop_list:
            shop_info = shop.find('div', {'class': 'txt'}).find('div', {'class': 'tit'})
            shop_info_title = shop_info.find('a')
            full_name = shop_info_title.get('title', '')
            if len(full_name) == 0:
                full_name = shop_info.find('h4').text
            if len(full_name) <= 0:
                continue
            shop_name = PAT.sub('', full_name)

            mean_price = None
            shop_comment = shop.find('div', {'class': 'comment'})
            if shop_comment is not None:
                mean_price = shop_comment.find('a', {'class': 'mean-price'})
                if mean_price is not None:
                    mean_price = mean_price.find('b')
                    if mean_price is not None:
                        mean_price = mean_price.text
            mean_price = mean_price[1:] if mean_price is not None else 0

            addr = ''
            addr_info = shop.find('div', {'class': 'tag-addr'})
            if addr_info is not None:
                addr_info = addr_info.findAll('span', {'class': 'tag'})
                if addr_info is not None and len(addr_info) > 0:
                    addr = addr_info[-1].text

            kouwei = None
            huanjing = None
            fuwu = None
            comment_list = shop.find('span', {'class': 'comment-list'})
            if comment_list is not None:
                comment_list = comment_list.findAll('span')
                for comment in comment_list:
                    if u'口味' in comment.text:
                        kouwei = comment.find('b')
                        if kouwei is not None:
                            kouwei = kouwei.text
                    elif u'环境' in comment.text:
                        huanjing = comment.find('b')
                        if huanjing is not None:
                            huanjing = huanjing.text
                    elif u'服务' in comment.text:
                        fuwu = comment.find('b')
                        if fuwu is not None:
                            fuwu = fuwu.text
            kouwei = kouwei if kouwei is not None else 0.0
            huanjing = huanjing if huanjing is not None else 0.0
            fuwu = fuwu if fuwu is not None else 0.0
            ret.append([category_name, shop_name, full_name, mean_price, addr, kouwei, huanjing, fuwu])
    except Exception as e:
        with open(os.path.join(DIAN_PING_DIR, 'error.csv'), 'a') as fs:
            writer = csv.writer(fs)
            writer.writerow([category_name, url, str(e)])
    return ret


def crawler(url, i):
    headers = {'Referer': HOST}
    headers['User-Agent'] = random.choice(USER_AGENT_CHOICES)
    r = requests.get(url, headers=headers, verify=False)
    time.sleep(0.5)
    if r.status_code != 200:
        print url, r.status_code
        return
    soup = BeautifulSoup(r.content)
    title = soup.find('title').text
    title = title[0:-8]
    first_nav = soup.find('li', {'data-key': '10'})
    second_nav = first_nav.find('div')
    category_list = second_nav.findAll('a')
    file_name = '%d_%s.txt' % (i + 1, title)
    print 'start crawling %d_%s' % (i + 1, title)
    with open(os.path.join(DIAN_PING_DIR, file_name), 'wb') as f:
        writer = csv.writer(f)
        for category in category_list[1:]:
            category_name = category.text
            category_root_url = category.get('href', '')
            r = requests.get(category_root_url, headers=headers, verify=False)
            time.sleep(0.5)
            if r.status_code != 200:
                print category_root_url, r.status_code
                continue
            soup = BeautifulSoup(r.content)
            num_tag = soup.find('span', {'class': 'num'})
            if num_tag is not None:
                num = num_tag.text
                try:
                    num = num[1:-1]
                    print num
                    num = int(num)
                    if num < 750:
                        for page in xrange(0, 50):
                            category_url = category_root_url + 'p%d' % (page + 1)
                            shop_list = fetch(category_url, category_name)
                            if shop_list is None:
                                break
                            for shop in shop_list:
                                writer.writerow(shop)
                    else:
                        region_tag = soup.find('div', {'id': 'region-nav'})
                        if region_tag is not None:
                            region_list = region_tag.findAll('a')
                            for region in region_list:
                                sub_url = region.get('href', '')
                                if sub_url is not None and len(sub_url) > 0:
                                    sub_url = HOST + (sub_url.split('#'))[0]
                                    r = requests.get(sub_url, headers=headers, verify=False)
                                    time.sleep(0.5)
                                    if r.status_code != 200:
                                        print sub_url, r.status_code
                                        continue
                                    soup = BeautifulSoup(r.content)
                                    num_tag = soup.find('span', {'class': 'num'})
                                    if num_tag is not None:
                                        num = num_tag.text
                                        try:
                                            num = num[1:-1]
                                            num = int(num)
                                            if num < 750:
                                                for page in xrange(0, 50):
                                                    category_url = sub_url + 'p%d' % (page + 1)
                                                    shop_list = fetch(category_url, category_name)
                                                    if shop_list is None:
                                                        break
                                                    for shop in shop_list:
                                                        writer.writerow(shop)
                                            else:
                                                sub_region_tag = soup.find('div', {'id': 'region-nav-sub'})
                                                if sub_region_tag is not None:
                                                    sub_region_list = sub_region_tag.findAll('a')
                                                    for sub_region in sub_region_list[1:]:
                                                        sub_sub_url = sub_region.get('href', '')
                                                        if sub_sub_url is not None and len(sub_sub_url) > 0 and '#' in sub_sub_url:
                                                            print sub_sub_url
                                                            sub_sub_url = HOST + (sub_sub_url.split('#'))[0]
                                                            for page in xrange(0, 50):
                                                                category_url = sub_sub_url + 'p%d' % (page + 1)
                                                                shop_list = fetch(category_url, category_name)
                                                                if shop_list is None:
                                                                    break
                                                                for shop in shop_list:
                                                                    writer.writerow(shop)
                                        except Exception as e1:
                                            print num, ' num is not valid1', str(e1)
                                            continue
                except Exception as e2:
                    print num, ' num is not valid2', str(e2)
                    continue
            print '%s_%s completed' %(title, category_name)
    print '%d_%s is completed' % (i + 1, title)


def city_crawler(url):
    headers = {'Referer': HOST}
    headers['User-Agent'] = random.choice(USER_AGENT_CHOICES)
    r = requests.get(url, headers=headers, verify=False)
    if r.status_code != 200:
        print 'city request error: %s' % url
        return
    soup = BeautifulSoup(r.content)
    city_tag = soup.find('ul', {'id': 'divArea'})
    city_set = set()
    if city_tag is not None:
        city_list = city_tag.findAll('a')
        with open(os.path.join(DIAN_PING_DIR, 'city_list.csv'), 'wb') as f:
            writer = csv.writer(f)
            for city in city_list:
                city_name = city.text
                if not u'更多'in city_name:
                    city_set |= set([city_name])
                    writer.writerow([city_name])
    print len(list(city_set))


if __name__ == '__main__':
    pool = Pool(processes=8)
    for i in [1724, 639, 924, 2406, 1254, 1956, 1526, 2341, 2339, 444, 1439, 402, 1441, 648, 680, 691, 2075, 735, 2056, 2200, 1052, 976, 843, 2167, 751, 1291, 
             362, 1128, 1235, 1203, 1422, 1664, 1562, 1803, 559, 2138, 2145, 913, 2047, 812, 1585, 2052, 805, 1272, 2079, 546, 656, 1051, 1929, 340, 420, 1110,
             1347, 2095, 729, 697, 2340, 587, 1137, 937, 1263, 2261, 2242, 547, 2245, 2033, 2054, 1046, 959, 2084, 1362, 653, 337, 2043, 973, 450, 1982, 1059,
             2053, 552, 935, 1975, 400, 1273, 925, 483, 728, 634, 1905, 844, 1812, 1707, 554, 2337, 416, 674, 2069, 569, 1535, 417, 1276, 427, 1644, 1246, 783,
             2184, 992, 2076, 1679, 638, 979, 313, 1048, 1459, 1261, 978, 418, 1297, 930, 1045, 867, 1650, 968, 1243, 429, 283, 321, 2042, 497, 1442, 1094,
             2040, 841, 1296, 1181, 1959, 956, 2309, 1963, 519, 1314, 967, 385, 498, 929, 1744, 1421, 1326, 2073, 1402, 946, 2164, 1990, 1251, 1044, 1049, 2237,
             502, 1143, 523, 549, 2165, 1313, 1446, 1346, 939, 459, 2064, 970, 1381, 923, 878, 954, 1670, 1248, 325, 1497, 931, 961, 1749, 1323, 1513, 936,
             1025, 652, 2338, 2004, 1271, 773, 1242, 1704, 2014, 977, 2055, 623, 645, 711, 2015, 556]:
        url = FOOD_URL % i
        pool.apply_async(crawler, (url, i - 1,))
    pool.close()
    pool.join()
#    city_crawler(CITY_URL)
#    url = FOOD_URL % (i + 1)
#    crawler(url, i)
