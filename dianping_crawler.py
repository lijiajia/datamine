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
from multiprocessing import Pool
from settings import BASE_DIR
from BeautifulSoup import BeautifulSoup
from env import USER_AGENT_CHOICES 

HOST = 'http://www.dianping.com'
FOOD_URL = 'http://www.dianping.com/search/category/%d/10'
DIAN_PING_DIR = os.path.join(BASE_DIR, 'dianping_data')

PAT = re.compile(ur'[\(\（].+店[\)\）]')

def crawler(url, i):
    print url
    headers = {'Referer': HOST}
    headers['User-Agent'] = random.choice(USER_AGENT_CHOICES)
    r = requests.get(url, headers=headers, verify=False)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.content)
    title = soup.find('title').text
    print title, len(title)
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
            category_url = category.get('href', '')
            for page in xrange(0, 50):
                category_url = category_url + 'p%d' % (page + 1)
                print category_url
                r = requests.get(category_url, headers=headers, verify=False)
                if r.status_code != 200:
                    break
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
                        print mean_price

                        addr = ''
                        addr_info = shop.find('div', {'class': 'tag-addr'})
                        if addr_info is not None:
                            addr_info = addr_info.findAll('span', {'class': 'tag'})
                            if addr_info is not None and len(addr_info) > 0:
                                addr = addr_info[-1].text
                        print addr

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
                        print category_name, shop_name, full_name, mean_price, addr, kouwei, huanjing, fuwu
                        break
                        writer.writerow([category_name, shop_name, full_name, mean_price, addr, kouwei, huanjing, fuwu])
                except Exception as e:
                    print category_name, category_url
                    print str(e)
                break
            print '%s_%s completed' %(title, category_name)
            break
    print '%d_%s is completed' % (i + 1, title)


if __name__ == '__main__':
    '''pool = Pool(processes=8)
    for i in xrange(0, 2610):
        url = FOOD_URL % (i + 1)
        pool.apply_async(crawler, (url, i,))
        break
    pool.close()
    pool.join()'''
    crawler(FOOD_URL % 1, 0)
