# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import re
import urllib

#Input

uniqueMappings = []
mappingSeg = []
uniqueMappingFile = open("uniqueMappings.tsv", "w+")
sourceDir = u"ConIPlogsessions/"
#targetDir = u"ConIPlogWoSub/"

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        #targetFile = open(targetDir + file, "w+")
        blockIdentifier = ""
        prevBlockIdentifier = ""
        urlblock = []
        pastUrl = ""
        for k in ipLines:
            ipLineParts = k.strip().split("\t")
            if not "target=root" in ipLineParts[2]:
                mapping = urllib.unquote(ipLineParts[2]).decode('utf8')
                #targetFile.write(ipLineParts[0] + "\t" + ipLineParts[1] + "\t" + mapping + "\n")
                mappingParts = re.split(r'[/#]', mapping)
                uniqueMapping = "|".join(mappingParts[0:len(mappingParts)-1])
                if not uniqueMapping in uniqueMappings:
                    print mappingParts
                    print uniqueMapping
                    uniqueMappings.append(uniqueMapping)
                    mappingSeg.append(mapping)

for mapping in range(len(uniqueMappings)):
    potIdentifier = uniqueMappings[mapping].split("|")
    uniqueMappingFile.write(uniqueMappings[mapping] + "\t" + mappingSeg[mapping] + "\t"+ potIdentifier[len(potIdentifier)-1] + "\n")


   
    