import os
import sys
import numpy as np
from scipy.sparse import * 
import sklearn.cluster as cluster

ontoTermMatrix = np.loadtxt(sys.argv[2], dtype=int)
print ontoTermMatrix.shape
ontoTermsFile = open(sys.argv[3])
ontoTerms = ontoTermsFile.readlines()
ontoTermsoutFile = open(sys.argv[4], "w+")

S = coo_matrix(ontoTermMatrix)
print S.shape

labeler = cluster.AgglomerativeClustering(n_clusters=int(sys.argv[1]))
labeler.fit(S.toarray())  

for (row, label) in enumerate(labeler.labels_):   
    print "row %d has label %d"%(row, label)
    ontoTermsoutFile.write(ontoTerms[int(row)+1].strip() + "\t" + str(label) + "\n" )