#!/usr/bin/env python
# coding=utf-8

from sklearn import cluster, datasets
from sklearn import neighbors 
import numpy as np
import pylab as pl
from scipy import misc
import matplotlib.pyplot as plt
from sklearn import decomposition

def test_1():
    iris = datasets.load_iris()
    k_means = cluster.KMeans(n_clusters=3)
    k_means.fit(iris.data)
    print k_means.labels_[::10]
    print iris.target[::10]

def test_2():
    lena = misc.lena().astype(np.float32)
    X = lena.reshape(-1, 1)
    k_means = cluster.KMeans(n_clusters=5)
    k_means.fit(X)
    values = k_means.cluster_centers_.squeeze()
    labels = k_means.labels_
    lena_compressed = np.choose(labels, values)
    lena_compressed.shape = lena.shape

    plt.gray()
    plt.imshow(lena_compressed)
    plt.show()

def test_3():
    iris = datasets.load_iris()
    pca = decomposition.PCA(n_components=2)
    pca.fit(iris.data)
    X = pca.transform(iris.data)
    print pl.scatter(X[:, 0], X[:, 1], c=iris.target)

def main():
    #test_1()
    test_2()
    #test_3()

if __name__ == '__main__':
    main()
