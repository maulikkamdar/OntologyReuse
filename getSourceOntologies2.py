# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import re
import urllib

#Input

noMappings = []
noMappingsFile = open("noMappings.tsv", "w+")
uniqueMappingFile = open("uniqueMappingsForm.tsv")
sourceDir = u"ConIPlogsessions/"
targetDir = u"ConIPlogWoSub/"

ontologyStats = {}
ontologyStatsFile = open("ontoStats.tsv", "w+")

stringPatterns = {}
for k in uniqueMappingFile:
    uniqueParams = k.strip().split("\t")
    stringPatterns[uniqueParams[0]] = uniqueParams[2]

uniqueMappingFile.close()


def addToFile(targetFile, file, ipLineParts, mapping, sourceonto):
    targetFile.write(ipLineParts[0] + "\t" + ipLineParts[1] + "\t" + mapping + "\t" + sourceonto + "\n")
    if sourceonto in ontologyStats:
        ontologyStats[sourceonto]["count"] = ontologyStats[sourceonto]["count"] + 1
        if not file in ontologyStats[sourceonto]["users"]:
            ontologyStats[sourceonto]["users"].append(file)
    else:
        print sourceonto
        ontologyStats[sourceonto] = {"count": 1, "users": []}
        ontologyStats[sourceonto]["users"].append(file)

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        targetFile = open(targetDir + file, "w+")
        blockIdentifier = ""
        prevBlockIdentifier = ""
        urlblock = []
        pastUrl = ""
        for k in ipLines:
            ipLineParts = k.strip().split("\t")
            if not "target=root" in ipLineParts[2]:
                mapping = urllib.unquote(ipLineParts[2]).decode('utf8')
                
                mappingParts = re.split(r'[/#]', mapping)
                uniqueMapping = "|".join(mappingParts[0:len(mappingParts)-1])
                foundMapping = False
                for pattern in stringPatterns:
                    if pattern in uniqueMapping:
                        #print stringPatterns[pattern]
                        addToFile(targetFile, file, ipLineParts, mapping, stringPatterns[pattern])
                        foundMapping = True
                        break

                if not foundMapping:
                    if "purl.obolibrary.org" in mappingParts:
                        mappingSubParts = re.split('[^0-9a-zA-Z]+', mapping)
                        print mappingSubParts[len(mappingSubParts)-2]
                        addToFile(targetFile, file, ipLineParts, mapping, mappingSubParts[len(mappingSubParts)-2])  
                        foundMapping = True 
                    elif "Ontology1298855822.owl" in mappingParts:
                        addToFile(targetFile, file, ipLineParts, mapping, "QIBO")  
                        foundMapping = True 
     
                if not foundMapping:
                    print uniqueMapping
                    noMappings.append(file + "\t" + k)
            else:
                targetFile.write(k)


for onto in ontologyStats:
    ontologyStatsFile.write(onto + "\t" + str(ontologyStats[onto]["count"]) + "\t" + str(len(ontologyStats[onto]["users"])) + "\t" + "-".join(ontologyStats[onto]["users"]) + "\n")

for k in noMappings:
    noMappingsFile.write(k)
    


   
    