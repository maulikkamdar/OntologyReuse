import os
import sys
import numpy
import scipy.sparse 
import sklearn.cluster  
import random
import pp
import time
import math

def find_centers(X, k):
    clusters = {}
    for i in range(k):
        clusters[i] = []

    S = scipy.sparse.coo_matrix(X)
    print S.shape
    labeler = sklearn.cluster.KMeans(n_clusters=k, max_iter=1000)
    labeler.fit(S.tocsr())
    for (row, label) in enumerate(labeler.labels_):
        clusters[label].append(X[int(row)])
    return (labeler.cluster_centers_, clusters)

def Wk(mu, clusters):
    K = len(mu)
    return sum([numpy.linalg.norm(mu[i]-c)**2/(2*len(c)) \
               for i in range(K) for c in clusters[i]])

def bounding_box(X):
    maxMinRange = []
    for i in range(X.shape[1]):
        #xmin, xmax = min(X,key=lambda a:a[i])[i], max(X,key=lambda a:a[i])[i]
        maxMinRange.append((0,1))
    return maxMinRange
 
def gap_statistic(X, k, job_server):
    #maxMinRange = bounding_box(X)
    # Dispersion for real distribution
    #Wks = numpy.zeros(len(ks))
    #Wkbs = numpy.zeros(len(ks))
    #sk = numpy.zeros(len(ks))
    mu, clusters = find_centers(X,k)
    Wks = numpy.log(Wk(mu, clusters))
        # Create B reference datasets
    B = 10
    print mu
    BWkbs = numpy.zeros(B)
    for i in range(B):
        Xb = []
        for n in range(X.shape[0]):
            ranRange = []
            for m in range(X.shape[1]):
                ranRange.append(random.randint(0,1))
            Xb.append(ranRange)
            if n == 0:
                print ranRange
        Xb = numpy.array(Xb)
        print i
        mu, clusters = find_centers(Xb,k)
        #job = job_server.submit(find_centers, (Xb, k,), (), ("numpy","scipy.sparse","sklearn.cluster"))
        #mu, clusters = job()
        BWkbs[i] = numpy.log(Wk(mu, clusters))

    #job_server.wait()
    print "Time elapsed: ", time.time() - start_time, "s"
    Wkbs = sum(BWkbs)/B
    sk = numpy.sqrt(sum((BWkbs-Wkbs)**2)/B)
    sk = sk*numpy.sqrt(1+1/B)
    return(Wks, Wkbs, sk)

ontoTermMatrix = numpy.loadtxt(sys.argv[1], dtype=int)
outputFile = open(sys.argv[2], "w+")

#ppservers = () # Add additional farmshare servers here?
#if sys.argv[4]:
#    job_server = pp.Server(16, ppservers=ppservers, secret=sys.argv[4])
#else:
#    job_server = pp.Server(16, ppservers=ppservers)

#print "Starting pp with", job_server.get_ncpus(), "workers"    
start_time = time.time()
print start_time    

#Input
#1 - ontoTermMatrix
#2 - outputfile
#3 - k
#4 - ppSecret

#logWks, logWkbs, sk = gap_statistic(ontoTermMatrix, int(sys.argv[3]), job_server)
logWks, logWkbs, sk = gap_statistic(ontoTermMatrix, int(sys.argv[3]), None)
outputFile.write(sys.argv[3] + "\t" + str(logWkbs) + "\t" + str(logWks) + "\t" + str(sk) + "\n")


