import os
import sys
import numpy as np



ontoCoccurFile = open(sys.argv[1])
ontoListFile = open(sys.argv[2])
ontoTermLines = ontoCoccurFile.readlines()
keyOntologies = ontoListFile.readlines()
ontoListFile.close()
ontoCoccurFile.close()

ontoTermMatrixFile = open(sys.argv[3], "w+")

ontoTermMatrix = np.zeros([len(ontoTermLines)-1,len(keyOntologies)], dtype=int)
ontoCount = 0
ontologyMapper = {}
ontoTerms = []

for i in keyOntologies:
    ontologyMapper[i.strip()]= ontoCount
    ontoCount = ontoCount + 1

print ontoCount
print ontologyMapper["GO"]

for i in range(len(ontoTermLines)):
    if i == 0:
        continue
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    ontoTerms.append(ontoTermParams[0].strip())
    print ontoTermParams[0].strip()
    inOntoLogies = ontoTermParams[3].strip().split(":-:")
    for j in inOntoLogies:
        ontoTermMatrix[i-1][ontologyMapper[j]] = 1

for i in range(len(ontoTermMatrix)):
    writeStr = ""
    for j in range(len(ontoTermMatrix[i])):
        if j == len(ontoTermMatrix[i])-1:
            writeStr = writeStr + str(ontoTermMatrix[i][j]) + "\n"
        else:
            writeStr = writeStr + str(ontoTermMatrix[i][j]) + "\t"
    ontoTermMatrixFile.write(writeStr)

