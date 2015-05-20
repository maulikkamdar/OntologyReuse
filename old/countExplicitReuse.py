import os
import sys

ontoCooccurFile = open(sys.argv[1])
ontoCooccurs = ontoCooccurFile.readlines()
ontoCooccurFile.close()

explicitCount = 0
for i in range(len(ontoCooccurs)):
    if i ==0:
        continue
    ontoCooccursParams = ontoCooccurs[i].strip().split("\t")
    explicitCount = explicitCount + int(ontoCooccursParams[2])

print explicitCount