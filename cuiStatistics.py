import os
import sys
cuiCoccurFile = open(sys.argv[1])
cuiCoccurTerms = cuiCoccurFile.readlines()
cuiCoccurFile.close()

cuiOutputFile = open(sys.argv[2], "w+")

for i in range(len(cuiCoccurTerms)):
    cuiParams = cuiCoccurTerms[i].strip().split("\t")
    print cuiParams[0]
    cuiOutputFile.write(cuiParams[0].strip() + "\t" + cuiParams[1].strip() + "\t" + str(len(cuiParams[1].split(":-:"))) + "\n")