import os
import sys
import datetime
import time
import urllib
import re
import math

ontologyTermsFile = open("../stage_rdf_dump/allOntoTermsWithSubClass.tsv")
ontoTermLines = ontologyTermsFile.readlines()
ontologyTermsFile.close()
ontoTerms = {}
imported = open("importedOntologies.tsv")
imports = [x.strip() for x in imported.readlines()]
imported.close()

targetFile = open("subclassFile_allred.tsv", "w+")

for k in range(len(ontoTermLines)):
    if k == 0:
        continue
    ontoParams = ontoTermLines[k].strip().split("\t")
    if not ontoParams[1] in imports:
        print ontoParams[1]
        continue
    if not ontoTerms.get(ontoParams[0]):
        identifierParts = re.split(r'[/#]', ontoParams[0])
        superclass = ontoParams[6].strip().split(":-:") if len(ontoParams) > 6 else []
        cui = ontoParams[4].strip() if len(ontoParams) > 4 else ""
        #print ontoParams[0]
        ontoTerms[ontoParams[0]] = {"uri": ontoParams[0], "label": [ontoParams[2]], "cui": cui, "identifier": identifierParts[len(identifierParts)-1], "superclass": superclass}
    else:
        superclass = ontoParams[6].strip().split(":-:") if len(ontoParams) > 6 else []
        # Considering the user has changed the properties during import
        for d in range(len(superclass)):
            if not superclass[d] in ontoTerms[ontoParams[0]]["superclass"]:
                ontoTerms[ontoParams[0]]["superclass"].append(superclass[d])
        if not ontoParams[2] in ontoTerms[ontoParams[0]]["label"]:
            ontoTerms[ontoParams[0]]["label"].append(ontoParams[2])
        
for param in ontoTerms:
    targetFile.write(param + "\t" + ontoTerms[param]["identifier"] + "\t" + ":-:".join(ontoTerms[param]["superclass"]) + "\t" + ontoTerms[param]["cui"] + "\t" +  ":-:".join(ontoTerms[param]["label"]) + "\n")

print len(ontoTerms)
