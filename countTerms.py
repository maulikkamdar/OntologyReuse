import os
import sys

ontoTermsFile = open(sys.argv[1])
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()

output = open(sys.argv[2], "w+")
ontology = {}

for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    if ontology.get(ontoTermParams[1]):
        ontology[ontoTermParams[1]] = ontology[ontoTermParams[1]] + 1
    else:
        ontology[ontoTermParams[1]] = 1

for onto in ontology:
    output.write(onto + "\t" + str(ontology[onto]) + "\n")

