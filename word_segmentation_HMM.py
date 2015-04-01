#!/usr/bin/env python
# coding=utf-8

from jieba import finalseg
from jieba.finalseg.prob_start import P


print P
res = finalseg.cut('我是一个好学生,活着真不容易,快干活泼')
print ','.join(res)
