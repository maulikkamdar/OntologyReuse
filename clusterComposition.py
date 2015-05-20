import os
import sys
import re
import numpy as np
import math

# Spectral cluster
ontoCoccurFile = open(sys.argv[1])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()

ontologies = {}
ontoCompoFile = open(sys.argv[2], "w+")

for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    ontoList = ontoTermParams[3].split(":-:")
    print i
    for onto in ontoList:
        if ontologies.get(onto):
            ontologies[onto] = ontologies[onto] + 1
        else:
            ontologies[onto] = 1


for onto in ontologies:
    ontoCompoFile.write(onto + "\t" + str(ontologies[onto]) + "\n")