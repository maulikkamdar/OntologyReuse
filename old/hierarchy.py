import numpy
import sys
from scipy.sparse import * 
import scipy.cluster.hierarchy as hcluster
import matplotlib.pyplot as plt

ontoTermMatrix = numpy.loadtxt(sys.argv[1], dtype=int)
ontoTermsFile = open(sys.argv[2])
ontoTerms = ontoTermsFile.readlines()
ontoTermsoutFile = open(sys.argv[3], "w+")

#S = coo_matrix(ontoTermMatrix)
#print S.shape

print ontoTermMatrix.shape
thresh = 1.5
clusters = hcluster.fclusterdata(ontoTermMatrix, thresh, criterion="distance")
print clusters

# plotting
plt.scatter(*numpy.transpose(data), c=clusters)
plt.axis("equal")
title = "threshold: %f, number of clusters: %d" % (thresh, len(set(clusters)))
plt.title(title)
plt.show()

#for (row, label) in enumerate(labeler.labels_):   
    #print "row %d has label %d"%(row, label)
    #ontoTermsoutFile.write(ontoTerms[int(row)+1].strip() + "\t" + str(label) + "\n" )
   
