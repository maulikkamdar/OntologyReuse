import os
import sys
import datetime
import time
import urllib
import re
import math

print "reading subclass information"
ontologyTermsFile = open("subclassFile_allred.tsv")
ontoTermLines = ontologyTermsFile.readlines()
ontologyTermsFile.close()

ontoTerms = {}
ontoLabels = {}
ontoCuis = {}

print "done"
for k in range(len(ontoTermLines)):
    ontoParams = ontoTermLines[k].strip().split("\t")
    if len(ontoParams) > 2:
        ontoTerms[ontoParams[0]] = {"uri": ontoParams[0], "identifier": ontoParams[1], "superclass": ontoParams[2].strip().split(":-:")}    


'''
cuiMapperFile = open("cuiMapperFile.tsv")
cuiMappings = cuiMapperFile.readlines()
cuiMapperFile.close()

labelMapperFile = open("labelMapperFile.tsv", "w+")
labels = labelMapperFile.readlines()
labelMapperFile.close()

for k in range(len(cuiMappings)):
    cuiParams = cuiMappings[k].strip().split("\t")
    ontoCuis[cuiParams[0]] = cuiParams[1].strip().split(":-:")

for k in range(len(labels)):
    labelParams = labels[k].strip().split("\t")
    ontoLabels[labelParams[0]] = labelParams[1].strip().split(":-:")
'''

print len(ontoTerms)
print len(ontoLabels)
print len(ontoCuis)


sourceDir = u"processedTimeBlocks/"
targetDir = u"annotatedTimeBlocks/"
count = 0

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        importedClasses = [ipLines[k].strip().split("\t")[0] for k in range(len(ipLines))]
    
        targetFile = open(targetDir + file, "w+")
		#registeredBlocks = []
        print file + "\t" + str(len(importedClasses))
        count = 0
        for k in range(len(ipLines)):
            ipLineParts = ipLines[k].strip().split("\t")
            if ipLineParts[0] in ontoTerms:
                superClasses = ontoTerms[ipLineParts[0]]["superclass"]
                hasSuperClass = []
                for upper in superClasses:
                    if upper in importedClasses:
                        hasSuperClass.append(upper)
                targetFile.write(ipLineParts[0] + "\t" + ipLineParts[1] + "\t" + ":-:".join(hasSuperClass) + "\n")
                count = count + 1
       	targetFile.close()


