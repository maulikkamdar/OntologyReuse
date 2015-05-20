import os
import sys
import re

ontoTermsFile = open(sys.argv[1])
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()

# Use Cui Stats file
cuiMatcherFile = open(sys.argv[2])
cuiLines = cuiMatcherFile.readlines()
cuiMatcherFile.close()

cuis = {}
ontologyUsingCuis = {}
cuiProportionFile = open(sys.argv[3], "w+")

for i in range(len(cuiLines)):
    cuisParams = cuiLines[i].strip().split("\t")
    cuis[cuisParams[0]] = int(cuisParams[2])
    
for i in range(len(ontoTermLines)):
    if i == 0:
        continue
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    if len(ontoTermParams) > 4:
        print ontoTermParams[4]
        if ontologyUsingCuis.get(ontoTermParams[1]):
            ontologyUsingCuis[ontoTermParams[1]]["count"] = ontologyUsingCuis[ontoTermParams[1]]["count"] + 1
        else:
            ontologyUsingCuis[ontoTermParams[1]] = {"count": 1, "sharedcount": 0, "range1": 0, "range2": 0, "range3": 0, "range4": 0, "range5": 0}
        if cuis.get(ontoTermParams[4]):
            ontologyUsingCuis[ontoTermParams[1]]["sharedcount"]= ontologyUsingCuis[ontoTermParams[1]]["sharedcount"] + 1
            if cuis[ontoTermParams[4]] <= 5:
                ontologyUsingCuis[ontoTermParams[1]]["range1"] = ontologyUsingCuis[ontoTermParams[1]]["range1"] + 1
            elif cuis[ontoTermParams[4]] > 5 and cuis[ontoTermParams[4]] <= 10:
                ontologyUsingCuis[ontoTermParams[1]]["range2"] = ontologyUsingCuis[ontoTermParams[1]]["range2"] + 1
            elif cuis[ontoTermParams[4]] > 10 and cuis[ontoTermParams[4]] <= 15:
                ontologyUsingCuis[ontoTermParams[1]]["range3"] = ontologyUsingCuis[ontoTermParams[1]]["range3"] + 1
            elif cuis[ontoTermParams[4]] > 15 and cuis[ontoTermParams[4]] <= 20:
                ontologyUsingCuis[ontoTermParams[1]]["range4"] = ontologyUsingCuis[ontoTermParams[1]]["range4"] + 1
            else:
                ontologyUsingCuis[ontoTermParams[1]]["range5"] = ontologyUsingCuis[ontoTermParams[1]]["range5"] + 1 
           
for onto in ontologyUsingCuis:
    cuiProportionFile.write(onto + "\t" + str(ontologyUsingCuis[onto]["count"]) + "\t" + str(ontologyUsingCuis[onto]["sharedcount"]) + "\t" + str(ontologyUsingCuis[onto]["range1"]) + "\t" + str(ontologyUsingCuis[onto]["range2"]) + "\t" + str(ontologyUsingCuis[onto]["range3"]) + "\t" + str(ontologyUsingCuis[onto]["range4"]) + "\t" + str(ontologyUsingCuis[onto]["range5"]) + "\n")