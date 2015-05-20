#!/usr/bin/python
# File: pkmeans.py
# Author: Maulik Kamdar
# Desc: This program performs Parallelized K-means Clustering to detect modules of co-occurring terms in biomedical ontologies
# Parallel Python Software: http://www.parallelpython.com

import math, sys, time
import numpy
import pp

class KMeansClusterer(object):
    def __init__(self, k, ontoTermFile, maxIt):
        self.ktimes = int(k)
        self.maxIt = int(maxIt)
        self.rtol = 1e-05 # Relative tolerance value used for comparing centroid positions
        self.atol = 1e-08 # Absolute tolerance value used for comparing centroid positions
        self.output = open('kmeans.out', 'w+') # output file - can be custom modified for user input
        self.clusters = [] # the clusters retrieved
        self.iterationCount = self.maxIt # total number of iterations taken
        self.ontoTermMatrix = numpy.loadtxt(ontoTermFile, dtype=float)
        self.centroidMatrix = []
        self.clusters = self.emptyClusters()
        self.ontologies = self.ontoTermMatrix.shape[1]
        print self.ontologies
        self.sliceWidth = int(len(self.ontoTermMatrix)/self.ktimes)
        self.ontoTermMatrix = numpy.column_stack((self.ontoTermMatrix, range(len(self.ontoTermMatrix))))

    def emptyClusters(self):
        clusters = []
        for i in range(self.ktimes):
            clusters.append([])
        return clusters

    def compCentroidPos(self, oldCentroids, newCentroids):
        return numpy.allclose(oldCentroids, newCentroids, self.rtol, self.atol)
    
def calEuclidDistance(terms, clusterer, cluster):
    centroids = clusterer.centroidMatrix
    retClusters =  clusterer.emptyClusters()
    for i in range(len(terms)):
        minimum = 10000000.0 #arbitrarily large number as I do not want to store previous minimum
        termCluster = cluster
        termVector = clusterer.ontoTermMatrix[terms[i]]
        termIndex = terms[i]
        p0 = numpy.delete(termVector, len(termVector)-1)
        for j in range(len(centroids)):
            currentMinimum = numpy.sum((p0-centroids[j])**2)
            if currentMinimum < minimum:
                termCluster = j
                minimum = currentMinimum
        retClusters[termCluster].append(termIndex)
    return retClusters
                
def calCentroid(points, clusterer):
    if len(points) == 0:
        return numpy.zeros([1,clusterer.ontologies], dtype=float) # Do not do this, you are grouping the clusters!
    else:
        return numpy.average(points[:,:clusterer.ontologies],0)    
            
def main():
    if len(sys.argv) < 4:
        print "You provided me %d arguments. Please provide me with atleast the names of the Data File, Number of centroids considered (k) and Maximum number of iterations considered (max.it), in that order. Also information on the centroids could be provided." % len(sys.argv)
        return 0
    clusterer = KMeansClusterer(sys.argv[1], sys.argv[2], sys.argv[3])
    ppservers = () # Add additional farmshare servers here?
    if sys.argv[4]:
        job_server = pp.Server(2*int(sys.argv[1]), ppservers=ppservers, secret=sys.argv[4])
    else:
        job_server = pp.Server(2*int(sys.argv[1]), ppservers=ppservers)

    print "Starting pp with", job_server.get_ncpus(), "workers"
    
    start_time = time.time()
    print start_time    
    for i in range(clusterer.ktimes):
        if i == clusterer.ktimes -1:
            slicedTerms = clusterer.ontoTermMatrix[i*clusterer.sliceWidth:]
            #print slicedTerms
            clusterer.clusters[i] = range(i*clusterer.sliceWidth, len(clusterer.ontoTermMatrix))
        else:
            slicedTerms = clusterer.ontoTermMatrix[i*clusterer.sliceWidth:(i+1)*clusterer.sliceWidth]
            clusterer.clusters[i] = range(i*clusterer.sliceWidth, (i+1)*clusterer.sliceWidth)
        print i
        job = job_server.submit(calCentroid, (slicedTerms, clusterer,), (numpy.average,), ("numpy",))
        clusterer.centroidMatrix.append(job())
    print "Time elapsed: ", time.time() - start_time, "s"

    iter = 0
    while True:
        oldClusters = clusterer.clusters
        clusterer.clusters = clusterer.emptyClusters()
        start_time = time.time()
        for i in range(clusterer.ktimes):
            job = job_server.submit(calEuclidDistance, (oldClusters[i], clusterer, i,), (numpy.sum, numpy.delete,), ("numpy",))
            retClusters = job()
            #Do you need this?
            for k in range(len(retClusters)):
                for l in retClusters[k]:
                    clusterer.clusters[k].append(l)
        
        job_server.wait()
        #print clusterer.clusters
        print "Time elapsed: ", time.time() - start_time, "s"
        oldCentroidMatrix = clusterer.centroidMatrix
        #print oldCentroidMatrix 
        clusterer.centroidMatrix = []
        for i in range(clusterer.ktimes):
            print len(clusterer.clusters[i])
            slicedTerms = numpy.empty([len(clusterer.clusters[i]), clusterer.ontologies+1], dtype=float)
            for k in range(len(clusterer.clusters[i])):
                slicedTerms[k] = clusterer.ontoTermMatrix[clusterer.clusters[i][k]]
            start_time = time.time()
            #print slicedTerms
            job = job.server.submit(calCentroid, (slicedTerms, clusterer,), (numpy.average,), ("numpy",))
                
            clusterer.centroidMatrix.append(job())
            print "Time elapsed: ", time.time() - start_time, "s"

        iter = iter + 1
        print iter

        #if iter > clusterer.maxIt or clusterer.compCentroidPos(oldCentroidMatrix, clusterer.centroidMatrix):
        if iter > clusterer.maxIt:
            for j in range(len(clusterer.clusters)):
                for x in clusterer.clusters[j]:
                    clusterer.output.write(str(x) + "\t" + str(j) + "\n")
            break
    return 1

if __name__ == '__main__':
    main()

