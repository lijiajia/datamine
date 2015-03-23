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


classifier = Pipeline([
    ('counter', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC())),
])

classifier.fit(X_train, y_train)
prediction = classifier.predict(X_test)

for i, label in enumerate(prediction):
    print X_test[i], '======>', ', '.join([target_names[_] for _ in label])

