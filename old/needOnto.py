import os
import sys

ontoTermsFile = open(sys.argv[1])
ontoTermsLines = ontoTermsFile.readlines()
ontoTermsFile.close()

ontoListFile = open("ontologyRest.tsv")
ontoList = [x.strip().split("\t")[0] for x in ontoListFile.readlines()]

notOnto = open("notOntoFile.tsv", "w+")
hasOnto = []

for i in range(len(ontoTermsLines)):
    ontology = ontoTermsLines[i].strip().split("\t")[1]
    if not ontology in hasOnto:
        print ontology
        hasOnto.append(ontology)


for k in ontoList:
    if not k in hasOnto:
        print k
        notOnto.write(k + "\n")

