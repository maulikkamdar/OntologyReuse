import os
import sys
import re
import numpy as np
import math

semSimMatrix = open(sys.argv[1])
semSimLines = semSimMatrix.readlines()
semSimMatrix.close()

# Spectral cluster
ontoCoccurFile = open(sys.argv[2])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()

clusters = {}
clusterSemSim = {}
clusterSemSimFile = open(sys.argv[3], "w+")

affinityMatrix = np.zeros([len(ontoTermLines), len(ontoTermLines)], dtype=float)

for i in range(len(semSimLines)):
    semSimParams = semSimLines[i].strip().split("\t")
    print semSimParams[3]
    affinityMatrix[int(semSimParams[0])][int(semSimParams[1])] = float(semSimParams[3])
    
for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    print ontoTermParams[5]
    if not clusters.get(ontoTermParams[5]):
        clusters[ontoTermParams[5]] = []
    clusters[ontoTermParams[5]].append(i)

for k in clusters:
    termIds = clusters[k]
    semSimSum = [0 for x in range(10)]
    for i in range(len(termIds)):
        for j in range(i+1, len(termIds)):
            index = int(math.ceil(affinityMatrix[i][j]*10))-1
            semSimSum[index] = semSimSum[index] + 1
    clusterSemSim[k] = semSimSum


for k in clusterSemSim:
    clusterSemSimFile.write(k + "\t" + "\t".join([str(x) for x in clusterSemSim[k]]) + "\t" + str(len(clusters[k])) + "\n")