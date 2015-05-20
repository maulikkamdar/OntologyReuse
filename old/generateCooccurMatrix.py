import os
import sys
import numpy

ontoCoccurFile = open(sys.argv[1]))
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()
termCooccurMatrixFile = open("termCooccurSpMatrixFile.tsv", "w+")
relLocator = {}

for i in range(len(ontoTermLines)):
    if i == 0:
       continue
    ontoPartsi = ontoTermLines[i].strip().split("\t")
    ontoPartsiOnto = ontoPartsi[3].strip().split(":-:")
    print ontoPartsi[0]

    countTracker = ""
    for j in range(len(ontoTermLines)):
        if j == 0:
           continue
        if relLocator.get(str(j) + "-" + str(i)):
            count = relLocator[str(j) + "-" + str(i)]
        else:
            ontoPartsj = ontoTermLines[j].strip().split("\t")
            ontoPartsjOnto = ontoPartsj[3].strip().split(":-:")
            count = 0
            for k in ontoPartsiOnto:
                if k in ontoPartsjOnto:
                    count = count+1 
            relLocator[str(i) + "-" +  str(j)] = count

        if count > 0:
            termCooccurMatrixFile.write(str(i) + "\t" + str(j) + "\t" + str(count) + "\n")
        
    

termCooccurMatrixFile.close()