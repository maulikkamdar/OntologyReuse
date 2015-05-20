import os
import sys
import datetime
import time
import urllib
import re
import math


sourceDir = u"annotatedTimeBlocks/"
targetDir = u"ultimateTimeBlocks/"
count = 0

singleTermCount = 0
subStructureCount = 0
subMinStructureLevel = 0
subMaxStructureLevel = 1000

validatedStructFile = open("validatedStructureFile.tsv", "w+")

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        targetFile = open(targetDir + file, "w+")
        subNodes = {}
        posSingleTerms = []
        print file
        count = 0
        for k in range(len(ipLines)):
            ipLineParts = ipLines[k].strip().split("\t")
            if len(ipLineParts) > 2:
                superNodes = ipLineParts[2].strip().split(":-:")
                #print superNodes
                for m in superNodes:
                    if subNodes.get(m):
                        subNodes[m].append(ipLineParts[0])
                    else: 
                        subNodes[m] = [ipLineParts[0]]
            else:
                posSingleTerms.append(ipLineParts[0])

        #rootNodes = []
        #targetFile.write("Single Terms \n")
        localTermCount = 0
        localStructureCount = 0
        localMinLevel = 1000
        localMaxLevel = 0

        for k in posSingleTerms:
            if not k in subNodes:
                targetFile.write(k + "\n")
                singleTermCount = singleTermCount + 1
                localTermCount = localTermCount + 1
            else:
                subClasses = subNodes[k]
                structureStr = k
                subStructureCount = subStructureCount + 1
                localStructureCount = localStructureCount + 1
                level = 0
                #print subClasses
                while (len(subClasses) > 0):
                    level = level + 1
                    structureStr = structureStr + "-->" + ":-:".join(subClasses)
                    newSubclasses = []
                    for m in subClasses:
                        if subNodes.get(m):
                            newSubclasses.extend(subNodes[m])
                    subClasses = newSubclasses

                if level < localMinLevel:
                    localMinLevel = level
                elif level > localMaxLevel:
                    localMaxLevel = level
                elif level < subMinStructureLevel:
                    subMinStructureLevel = level
                elif level > subMaxStructureLevel:
                    subMaxStructureLevel = level

                targetFile.write(structureStr + "\n")

        validatedStructFile.write(file + "\t" + str(localTermCount) + "\t" + str(localStructureCount) + "\t" + str(localMinLevel) + "\t" + str(localMaxLevel) + "\n")

print str(singleTermCount) + "\t" + str(subStructureCount) + "\t" + str(subMinStructureLevel) + "\t" + str(subMaxStructureLevel)
