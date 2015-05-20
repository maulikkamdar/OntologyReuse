import os
import sys
import datetime
import time
import urllib
import re
import math

ontologyTermsFile = open("subclassFile_allred.tsv")
ontoTermLines = ontologyTermsFile.readlines()
ontologyTermsFile.close()

cuiMapperFile = open("cuiMapperFile.tsv")
cuiMappings = cuiMapperFile.readlines()
cuiMapperFile.close()

labelMapperFile = open("labelMapperFile.tsv", "w+")
labels = labelMapperFile.readlines()
labelMapperFile.close()

ontoTerms = {}
ontoLabels = {}
ontoCuis = {}

for k in range(len(ontoTermLines)):
    ontoParams = ontoTermLines[k].strip().split("\t")
    if len(ontoParams) > 2:
        ontoTerms[ontoParams[0]] = {"uri": ontoParams[0], "identifier": ontoParams[1], "superclass": ontoParams[2].strip().split(":-:")}    

for k in range(len(cuiMappings)):
    cuiParams = cuiMappings[k].strip().split("\t")
    ontoCuis[cuiParams[0]] = cuiParams[1].strip().split(":-:")

for k in range(len(labels)):
    labelParams = labels[k].strip().split("\t")
    ontoLabels[labelParams[0]] = labelParams[1].strip().split(":-:")

print len(ontoTerms)
print len(ontoLabels)
print len(ontoCuis)

sourceDir = u"ConIPlogWoSub/"
targetDir = u"ipTimeBlocks/"

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        #if not file == "60.45.182.232":
        #    continue
        print file
        block = 0
        targetFile = open(targetDir + file + "-" + str(block), "w+")
        blockIdentifier = ""
        prevBlockIdentifier = ""
        urlblock = []
        pastUrl = ""
        pastpastUrl = ""

        pastTime = 0.0
        networkTime = 0.0
        avgTime = 0.0
        counts = 0
        receivedOntPath = False
        sourceOntology = ""
        prevRestCall = ""
        currentDrag = 0

        for k in range(len(ipLines)):
            ipLineParts = ipLines[k].strip().split("\t")
            if "target=root" in ipLineParts[2]:
                blockIdentifier = ipLineParts[2].split("&target=root")[0]
                pastTime = float(ipLineParts[0])
                receivedOntPath = False
                mainSuperClass = []
                pathFollowed = []
                networkTime = 0.0
                counts = 0
                ongoingDepth = ""
                targetFile.write(ipLines[k].strip() + "\t\t----------\n")
            else:
                #OUtput the old block as the new block identifier has changed
                if prevBlockIdentifier != blockIdentifier and prevBlockIdentifier != "":
                    if pastTime > 300.0: # Set threshold to 5 minutes for inactivity between two blocks
                        #Check if the source ontology still remains the same - assume IP+source Ontology combination
                        if k < len(ipLines):
                            nextLineParts = ipLines[k+1].strip().split("\t")
                            if len(nextLineParts) > 3:
                                if not nextLineParts[3] == sourceOntology:
                                    targetFile.close()
                                    block = block + 1
                                    targetFile = open(targetDir + file + "-" + str(block), "w+")
                    urlblock = []
                else:
                    url = ipLineParts[2]
                    timedif = float(ipLineParts[0])

                    if receivedOntPath:
                        #print url + str(math.ceil(networkTime))
                        if url == pastUrl and timedif > math.ceil(avgTime) + 1 and not url in urlblock: # Set threshold for single term import 
                            targetFile.write("Single Term Import\n")
                            targetFile.write(ipLines[k])
                            currentDrag = 0
                            urlblock.append(url)
                        elif timedif < math.ceil(avgTime) + 1: # Set threshold for subtree import 
                            if currentDrag == 0:
                                targetFile.write("Subtree begins here\n")
                                pathFollowed = []
                                if ontoTerms.get(pastUrl):
                                    pathFollowed = ontoTerms[pastUrl]["superclass"]
                                    path = ["-" for x in range(len(pathFollowed))]
                                    targetFile.write(prevRestCall.strip() + "\t"+ "".join(path) +"\n")
                                else:
                                    targetFile.write(prevRestCall)
                                pathFollowed.append(pastUrl)
                                urlblock.append(url)
                            #if not url in urlblock:
                            currentSuperClass = []
                            if ontoTerms.get(url):
                                currentSuperClass = ontoTerms[url]["superclass"]
                            path = ["-" for x in range(len(set(pathFollowed) & set(currentSuperClass)))]
                            if len(path) > 1:
                                print "".join(path)
                            targetFile.write(ipLines[k].strip() + "\t"+ "".join(path) +"\n")
                            pathFollowed.append(url)
                            currentDrag = currentDrag + 1
                            urlblock.append(url)
                        else:
                            currentDrag = 0
                            
                        pastUrl = url
                        pastpastUrl = pastUrl
                        prevRestCall = ipLines[k]
                    else:
                        normalizedUrl = re.sub('[^0-9a-zA-Z]+', '', url)
                        normPattern = re.sub('[^0-9a-zA-Z]+', '', blockIdentifier)
                        networkTime = networkTime + timedif  
                        counts = counts + 1   
                        if normPattern in normalizedUrl:
                            receivedOntPath = True
                            avgTime = networkTime/counts
                        
                prevBlockIdentifier = blockIdentifier
            #if k > 200:
            #    break

            #if k == len(ipLines)-1:
            #    for m in urlblock:
            #        targetFile.write(urlblock[m]["timedif"] + "\t" + urlblock[m]["time"] + "\t" + urlblock[m]["url"] + "\t" + urlblock[m]["source"] + "\n")
            #    targetFile.close()
