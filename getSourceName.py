import os
import sys
import datetime
import time
import urllib
import re
import math

print "start"
sourceDir = u"ultimateTimeBlocks/"
targetDir = u"sourceTermDir/"
ontologyTermsFile = open("subclassFile_allred.tsv")
ontoTermLines = ontologyTermsFile.readlines()
ontologyTermsFile.close()
ontoTerms = {}

for k in range(len(ontoTermLines)):
    ontoParams = ontoTermLines[k].strip().split("\t")
    if len(ontoParams) > 4:
        conceptLabels = ontoParams[4].strip().split(":-:")
        ontoTerms[ontoParams[0]] = conceptLabels[0]

print "done"
for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        targetFile = open(targetDir + file, "w+")
        print file
        for k in range(len(ipLines)):
            ipLinesParams = ipLines[k].strip().split("-->")
            if ontoTerms.get(ipLinesParams[0]):
                targetFile.write(ipLinesParams[0] + "\t" + ontoTerms[ipLinesParams[0]] + "\n")


        