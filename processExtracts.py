import os
import sys
import datetime
import time
import urllib
import re
import math


sourceDir = u"newTimeBlocks/"
singleImportFile = open("singleImportFile.tsv", "w+")
targetDir = u"processedTimeBlocks/"
singleTerms = {}
subTreeCount = 0
subTreeCountFile = open("subTreeCount.tsv", "w+")

def inputSingleTerm(term, fileName):
    if not term in singleTerms:
        singleTerms[term] = [fileName]
    elif not fileName in singleTerms.get(term):
        singleTerms[term].append(fileName)


for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        if len(ipLines) == 0:
            os.remove(sourceDir + file) 
        print file
        urlBlock = {}
        subTreeCount = 0

        localBlock = []
        targetFile = open(targetDir + file, "w+")
        for k in range(len(ipLines)):
            if ipLines[k].strip() == "Single Term Import":
                nextLineParams = ipLines[k+1].strip().split("\t")
                inputSingleTerm(nextLineParams[2], file)
                if len(localBlock) == 1:
                    for url in localBlock:
                        inputSingleTerm(url, file)                           
                localBlock = []
            elif ipLines[k].strip() == "Subtree begins here":
                subTreeCount = subTreeCount+1
                if len(localBlock) == 1:
                    for url in localBlock:
                        inputSingleTerm(url, file)   
                localBlock = []
                print subTreeCount
            else:
                ipParams = ipLines[k].strip().split("\t")
                if len(localBlock) < 3:
                    if not ipParams[2] in localBlock:
                       localBlock.append(ipParams[2])
                if not ipParams[2] in urlBlock:
                    urlBlock[ipParams[2]] = 1
                else:
                    urlBlock[ipParams[2]] = urlBlock[ipParams[2]] + 1
               
        for url in urlBlock:
            if len(urlBlock) == 1:
                inputSingleTerm(url, file)
            targetFile.write(url + "\t" + str(urlBlock[url]) +  "\n")

        subTreeCountFile.write(file + "\t" + str(subTreeCount) + "\n")
        targetFile.close()

for term in singleTerms:
     singleImportFile.write(term + "\t" + str(len(singleTerms[term])) + "\t" + ":-:".join(singleTerms[term]) + "\n")


print subTreeCount