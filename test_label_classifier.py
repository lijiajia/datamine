#!/usr/bin/env python
# coding=utf-8

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier

X_train = [
    '中国在亚洲',
    '中国的菜非常好吃',
    '北京是中国的首都',
    '毛主席是中国的主席',
    '中国的天气比较差',
    '我爱中国',
    '美国是资本主义国家',
    '美国在北美洲',
    '奥巴马是美国的总统',
    '美国有很多篮球明星',
    '很多人想去美国',
    '美国的天气很好',
    '中国的人口比美国多',
    '美国的人均收入比中国高',
]

y_train = [
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [0, 1],
    [0, 1],
]

X_test = [
    '欢迎来到中国',
    '美国欢迎你',
    '中国欢迎你，美国也欢迎你',
]

target_names = ['中华人民共和国', '美利坚合众国']

count_v1 = CountVectorizer(stop_words='english', max_df=0.5)
counts_train = count_v1.fit_transform(X_train)
print 'The shape of train is ' + repr(counts_train.shape)

count_v2 = CountVectorizer(vocabulary=count_v1.vocabulary_)
counts_test = count_v2.fit_transform(X_test)
print 'the shape of test is ' + repr(counts_test.shape)

tfidftransformer = TfidfTransformer()

tfidf_train = tfidftransformer.fit(counts_train).transform(counts_train)
tfidf_test = tfidftransformer.fit(counts_test).transform(counts_test)


print tfidf_train
print tfidf_test
