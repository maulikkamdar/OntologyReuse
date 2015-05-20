import sys
import numpy
from sklearn import svm, decomposition

ontoTermMatrix = numpy.loadtxt(sys.argv[1], dtype=int)
output = open(sys.argv[3], "w+")

pca = decomposition.PCA(n_components=int(sys.argv[2]))
pca.fit(ontoTermMatrix)
new_X = pca.transform(ontoTermMatrix)

for k in range(len(new_X)):
    decStr = "\t".join([str(new_X[k,i]) for i in range(int(sys.argv[2]))])  + "\n"
    output.write(decStr)

output.close()
    

#ycolors = [hexarray[i] for i in ontoTermClusters]
#pl.scatter(new_X[:, 0], new_X[:, 1], c=hexMatrix, s=50)
#pl.show()