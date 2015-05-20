import os
import sys
import datetime
import time
import urllib
import re
import math

ontologyTermsFile = open("subclassFile_allred.tsv")
ontoTermLines = ontologyTermsFile.readlines()
ontologyTermsFile.close()
ontoTerms = {}
ontoLabels = {}
ontoCuis = {}

cuiMapperFile = open("cuiMapperFile.tsv", "w+")
labelMapperFile = open("labelMapperFile.tsv", "w+")

for k in range(len(ontoTermLines)):
    ontoParams = ontoTermLines[k].strip().split("\t")
    if len(ontoParams) > 4:
        conceptLabels = ontoParams[4].strip().split(":-:")
        for label in conceptLabels:
            normLabel = re.sub('[^0-9a-zA-Z]+', '', label).lower()
            print str(k) + "\t" + normLabel
            if not ontoLabels.get(normLabel):
                ontoLabels[normLabel] = [ontoParams[0]]
            elif not ontoParams[0] in ontoLabels.get(normLabel):
                ontoLabels[normLabel].append(ontoParams[0])

        cui = ontoParams[3].strip()
        normCui = cui.lower()
        if not ontoCuis.get(cui):
            ontoCuis[cui] = [ontoParams[0]]
        elif not ontoParams[0] in ontoCuis.get(cui):
            ontoCuis[cui].append(ontoParams[0])


for label in ontoLabels:
    labelMapperFile.write(label + "\t" + ":-:".join(ontoLabels[label]) + "\n")

for cui in ontoCuis:
    cuiMapperFile.write(cui + "\t" + ":-:".join(ontoCuis[cui]) + "\n")
