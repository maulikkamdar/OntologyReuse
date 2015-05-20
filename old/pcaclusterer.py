import sys
import colorsys
import numpy
from sklearn import svm, decomposition
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pl
import matplotlib as mpl

def get_N_HexCol(N):
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in xrange(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x*255),colorsys.hsv_to_rgb(*rgb))
        hex_out.append("#" + "".join(map(lambda x: chr(x).encode('hex'),rgb)))
    return hex_out


hexarray = get_N_HexCol(100)
print hexarray[1]
ontoTermMatrix = numpy.loadtxt(sys.argv[1], dtype=int)
ontoTermsFile = open(sys.argv[2])
ontoTerms = ontoTermsFile.readlines()
ontoTermClusters = [int(x.strip().split("\t")[4]) for x in ontoTerms]

subsetMatrix = []
hexMatrix = []
for i in range(len(ontoTermClusters)):
    if ontoTermClusters[i] in range(0,5):
        subsetMatrix.append(ontoTermMatrix[i])
        hexMatrix.append(hexarray[ontoTermClusters[i]])
pca = decomposition.PCA(n_components=2)
pca.fit(ontoTermMatrix)
new_X = pca.transform(subsetMatrix)
#ycolors = [hexarray[i] for i in ontoTermClusters]
pl.scatter(new_X[:, 0], new_X[:, 1], c=hexMatrix, s=50)
pl.show()