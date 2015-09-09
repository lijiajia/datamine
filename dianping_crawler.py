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
DIAN_PING_DIR = os.path.join(BASE_DIR, 'biz_addr')

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
            detail_addr = ''
            addr_info = shop.find('div', {'class': 'tag-addr'})
            if addr_info is not None:
                short_addr_info = addr_info.findAll('span', {'class': 'tag'})
                if short_addr_info is not None and len(short_addr_info) > 0:
                    addr = short_addr_info[-1].text
                detail_addr_info = addr_info.find('span', {'class': 'addr'})
                if detail_addr_info is not None:
                    detail_addr = detail_addr_info.text

            #kouwei = None
            #huanjing = None
            #fuwu = None
            #comment_list = shop.find('span', {'class': 'comment-list'})
            #if comment_list is not None:
            #    comment_list = comment_list.findAll('span')
            #    for comment in comment_list:
            #        if u'口味' in comment.text:
            #            kouwei = comment.find('b')
            #            if kouwei is not None:
            #                kouwei = kouwei.text
            #        elif u'环境' in comment.text:
            #            huanjing = comment.find('b')
            #            if huanjing is not None:
            #                huanjing = huanjing.text
            #        elif u'服务' in comment.text:
            #            fuwu = comment.find('b')
            #            if fuwu is not None:
            #                fuwu = fuwu.text
            #kouwei = kouwei if kouwei is not None else 0.0
            #huanjing = huanjing if huanjing is not None else 0.0
            #fuwu = fuwu if fuwu is not None else 0.0
            ret.append([category_name, shop_name, full_name, mean_price, addr, detail_addr])
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
    for i in xrange(110, 2600):
        url = FOOD_URL % i
        pool.apply_async(crawler, (url, i - 1,))
    pool.close()
    pool.join()
#    city_crawler(CITY_URL)
#    url = FOOD_URL % (i + 1)
#    crawler(url, i)
