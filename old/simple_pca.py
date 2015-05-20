import sys
import colorsys
import numpy
from sklearn import svm, decomposition
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pl
import matplotlib as mpl

ontoTermMatrix = numpy.loadtxt(sys.argv[1], dtype=int)
pca = decomposition.PCA(n_components=2)
pca.fit(ontoTermMatrix)
new_X = pca.transform(ontoTermMatrix)
#ycolors = [hexarray[i] for i in ontoTermClusters]
pl.scatter(new_X[:, 0], new_X[:, 1], s=50)
pl.show()