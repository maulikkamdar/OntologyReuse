import os
import sys
import numpy as np
from scipy.sparse import * 
from sklearn.cluster import KMeans  
import random

def find_centers(X, k):
    clusters = {}
    for i in range(k):
        clusters[i] = []

    S = coo_matrix(X)
    print S.shape
    labeler = KMeans(n_clusters=k, max_iter=1000)
    labeler.fit(S.tocsr())
    for (row, label) in enumerate(labeler.labels_):
        clusters[label].append(X[int(row)])
    return (labeler.cluster_centers_, clusters)

def Wk(mu, clusters):
    K = len(mu)
    return sum([np.linalg.norm(mu[i]-c)**2/(2*len(c)) \
               for i in range(K) for c in clusters[i]])

def bounding_box(X):
    xmin, xmax = min(X,key=lambda a:a[0])[0], max(X,key=lambda a:a[0])[0]
    ymin, ymax = min(X,key=lambda a:a[1])[1], max(X,key=lambda a:a[1])[1]
    return (xmin,xmax), (ymin,ymax)
 
def gap_statistic(X):
    (xmin,xmax), (ymin,ymax) = bounding_box(X)
    # Dispersion for real distribution
    ks = range(1,10)
    Wks = np.zeros(len(ks))
    Wkbs = np.zeros(len(ks))
    sk = np.zeros(len(ks))
    for indk, k in enumerate(ks):
        print k
        mu, clusters = find_centers(X,k)
        Wks[indk] = np.log(Wk(mu, clusters))
        # Create B reference datasets
        B = 10
        BWkbs = np.zeros(B)
        for i in range(B):
            Xb = []
            for n in range(len(X)):
                Xb.append([random.uniform(xmin,xmax),
                          random.uniform(ymin,ymax)])
            Xb = np.array(Xb)
            mu, clusters = find_centers(Xb,k)
            BWkbs[i] = np.log(Wk(mu, clusters))
        Wkbs[indk] = sum(BWkbs)/B
        sk[indk] = np.sqrt(sum((BWkbs-Wkbs[indk])**2)/B)
    sk = sk*np.sqrt(1+1/B)
    return(ks, Wks, Wkbs, sk)

ontoTermMatrix = np.loadtxt(sys.argv[1], dtype=int)
outputFile = open("optimumK.tsv", "w+")
ks, logWks, logWkbs, sk = gap_statistic(ontoTermMatrix)
for i in ks:
    print i
    outputFile.write(str(i) + "\t" + str(logWkbs[i-1]) + "\t" + str(logWks[i-1]) + "\t" + str(sk[i-1]) + "\n")
