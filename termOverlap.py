import os
import re
import sys

ontoTermsFile = open(sys.argv[1])
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()
ontoLabels = {}
termOverlapFile = open(sys.argv[2], "w+")

for i in range(len(ontoTermLines)):
    if i == 0:
        continue
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    label = re.sub('[^0-9a-zA-Z]+', '', ontoTermParams[2].strip()).lower()
    if ontoLabels.get(label):
        if ontoTermParams[1].strip() in ontoLabels[label][1]:
            continue
        ontoLabels[label][0] = ontoLabels[label][0] + 1
    else:
        print label
        ontoLabels[label] = [1, [], []]
    ontoLabels[label][1].append(ontoTermParams[1].strip())
    if not ontoTermParams[0].strip() in ontoLabels[label][2]:
        ontoLabels[label][2].append(ontoTermParams[0].strip())

for label in ontoLabels:
    if ontoLabels[label][0] > 1:
        termOverlapFile.write(label + "\t" + str(ontoLabels[label][0]) + "\t" + ":-:".join(ontoLabels[label][1]) + "\t" + ":-:".join(ontoLabels[label][2]) + "\n")
        
    