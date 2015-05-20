import os
import sys
import datetime
import time
import urllib
import re
import math

sourceDir = u"ConIPlogWoSub/"
targetDir = u"newTimeBlocks/"
termsImported = {}
termFile = open("importedTerms.tsv", "w+")

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        ipLines = ipFile.readlines()
        ipFile.close()
        #if not file == "24.193.146.13":
        #    continue
        print file
        block = 0
        targetFile = open(targetDir + file + "-" + str(block) +".tsv", "w+")
        blockIdentifier = ""
        prevBlockIdentifier = ""
        urlblock = []
        pastUrl = ""
        pastpastUrl = ""
        pathCount = 0
        pastTime = 0.0
        networkTime = 0.0
        avgTime = 0.0
        counts = 0
        receivedOntPath = False
        sourceOntology = "" 
        prevOntology = ""
        prevRestCall = ""
        currentDrag = 0
        writtenLines = 0

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
                currentDrag = 0
                pathCount = 0
                #targetFile.write(ipLines[k].strip() + "\t\t----------\n")
            else:
                #OUtput the old block as the new block identifier has changed
                if prevBlockIdentifier != blockIdentifier and prevBlockIdentifier != "":
                    if pastTime > 300.0: # Set threshold to 5 minutes for inactivity between two blocks
                        #Check if the source ontology still remains the same - assume IP+source Ontology combination
                        if k < len(ipLines)-1:
                            nextLineParts = ipLines[k+1].strip().split("\t")
                            if len(nextLineParts) > 3:
                                if not nextLineParts[3] == sourceOntology and writtenLines > 0:
                                    targetFile.close()
                                    block = block + 1
                                    writtenLines = 0
                                    targetFile = open(targetDir + file + "-" + str(block)+".tsv", "w+")
                        else:
                            targetFile.close()
                            block = block + 1
                            targetFile = open(targetDir + file + "-" + str(block), "w+")
                    urlblock = []
                else:
                    url = ipLineParts[2]
                    timedif = float(ipLineParts[0])

                    if receivedOntPath:
                        sourceOntology = ipLineParts[3]
                        if pathCount > 0:
                            if url == pastUrl and timedif > math.ceil(avgTime) + 2 and not url in urlblock: # Set threshold for single term import 
                                targetFile.write("Single Term Import\n")
                                targetFile.write(ipLines[k])
                                writtenLines = writtenLines+1
                                currentDrag = 0
                                urlblock.append(url)
                                if not url in termsImported:
                                    termsImported[url] = [file]
                                elif not file in termsImported.get(url):
                                    termsImported[url].append(file)
                            elif timedif < math.ceil(avgTime) + 2 and prevOntology == sourceOntology: # Set threshold for subtree import 
                                if currentDrag == 0:
                                    targetFile.write("Subtree begins here\n")
                                    targetFile.write(prevRestCall)
                                    writtenLines = writtenLines+1
                                    urlblock.append(url)

                                targetFile.write(ipLines[k].strip() +"\n")
                                writtenLines = writtenLines+1
                                currentDrag = currentDrag + 1
                                urlblock.append(url)
                                if not url in termsImported:
                                    termsImported[url] = [file]
                                elif not file in termsImported.get(url):
                                    termsImported[url].append(file)
                            else:
                                currentDrag = 0
                            
                            pastUrl = url
                            pastpastUrl = pastUrl
                            prevRestCall = ipLines[k]
                            prevOntology = sourceOntology
                        pathCount = 1
                    else:
                        normalizedUrl = re.sub('[^0-9a-zA-Z]+', '', url)
                        normPattern = re.sub('[^0-9a-zA-Z]+', '', blockIdentifier)
                        networkTime = networkTime + timedif  
                        counts = counts + 1   
                        if normPattern in normalizedUrl:
                            receivedOntPath = True
                            pastUrl = url
                            pathCount = 0
                            avgTime = networkTime/counts
                        
                prevBlockIdentifier = blockIdentifier
            #print k
            #if k == len(ipLines)-1:
            #    targetFile.close()


for term in termsImported:
    termFile.write(term + "\t" + str(len(termsImported[term])) + "\t" + ":-:".join(termsImported[term]) + "\n")
    