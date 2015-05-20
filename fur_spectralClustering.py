import os
import sys
import numpy as np
from sklearn.cluster import SpectralClustering

ontoCoccurFile = open(sys.argv[1])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()

semSimMatrix = open(sys.argv[2])
semSimLines = semSimMatrix.readlines()
semSimMatrix.close()

w1 = float(sys.argv[3])
w2 = float(sys.argv[4])
ontoTermsoutFile = open(sys.argv[5], "w+")

print len(ontoTermLines)
affinityMatrix = np.zeros([len(ontoTermLines), len(ontoTermLines)], dtype=float)

for i in range(len(semSimLines)):
    semSimParams = semSimLines[i].strip().split("\t")

    ontoPartsi = ontoTermLines[int(semSimParams[0])].strip().split("\t")
    ontoPartsiOnto = ontoPartsi[3].strip().split(":-:")
    ontoPartsj = ontoTermLines[int(semSimParams[1])].strip().split("\t")
    ontoPartsjOnto = ontoPartsj[3].strip().split(":-:")
    commonOnto = len(list(set(ontoPartsiOnto) & set(ontoPartsjOnto)))

    score = commonOnto*(w1*float(semSimParams[2]) + w2*float(semSimParams[3]))
    print score
    affinityMatrix[int(semSimParams[0])][int(semSimParams[1])] = score


print "Lets try spectral, spectral, we are gonna try spectral"
afc = SpectralClustering(n_clusters=int(sys.argv[6]), affinity="precomputed", assign_labels="discretize")
afc.fit(affinityMatrix)


for (row, label) in enumerate(afc.labels_):   
    print "row %d has label %d"%(row, label)
    ontoTermsoutFile.write(ontoTermLines[int(row)].strip() + "\t" + str(label) + "\n" )
    

