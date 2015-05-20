import os
import sys
import numpy as np



ontoCoccurFile = open(sys.argv[1])
ontoTermLines = ontoCoccurFile.readlines()
ontoListile = open(sys.argv[2], "w+")

ontoList = []

for i in range(len(ontoTermLines)):
    if i == 0:
        continue
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    print ontoTermParams[0].strip()
    inOntoLogies = ontoTermParams[3].strip().split(":-:")
    for j in inOntoLogies:
        if not j in ontoList:
            ontoList.append(j)
            print j

print len(ontoList)
for i in ontoList:
    ontoListile.write(i + "\n")
