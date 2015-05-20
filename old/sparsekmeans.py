import numpy
import sys
from scipy.sparse import * 
from sklearn.cluster import KMeans  

ontoTermMatrix = numpy.loadtxt(sys.argv[2], dtype=int)
ontoTermsFile = open(sys.argv[3])
ontoTerms = ontoTermsFile.readlines()
ontoTermsoutFile = open(sys.argv[4], "w+")

S = coo_matrix(ontoTermMatrix)
print S.shape
labeler = KMeans(n_clusters=int(sys.argv[1]), max_iter=1000)
labeler.fit(S.tocsr())  

for (row, label) in enumerate(labeler.labels_):   
    print "row %d has label %d"%(row, label)
    ontoTermsoutFile.write(ontoTerms[int(row)+1].strip() + "\t" + str(label) + "\n" )
   
