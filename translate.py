#!/usr/bin/env python
# coding=utf-8

import urllib
import requests
from BeautifulSoup import BeautifulSoup


def translate(text):
    text_1 = text
    values = {'hl': 'zh-CN', 'ie': 'UTF-8', 'text': text_1, 'langpair': "'en'|'zh-CN'", 'sl': 'en', 'tl': 'zh-CN', 'js': 'n', 'prev': '_t'}
    url = 'http://translate.google.cn/translate_t'
    data = urllib.urlencode(values)
    headers = {'User-Agent': 'Mozilla/4.0 (compatible: MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'}
    proxies = {'http': 'http://fq.mioffice.cn:3128'}
    r = requests.post(url, data=data, headers=headers, proxies=proxies)
    print r.status_code
    html = r.content.decode('gb2312', 'ignore')
    soup = BeautifulSoup(html)
    result_box = soup.find('span', {'id': 'result_box'})
    if result_box is not None:
        return result_box.text.strip('')

if __name__ == '__main__':
    text_1 = 'Hello, my name is Lijiajia. Nice to meet you!'
    print ('The input text: %s' % text_1)
    text_2 = translate(text_1)
    if text_2 is not None:
        print 'The output text: %s' % text_2.strip("'")
