import os
import re
import sys

# CUI Match File cuiMatchTerms.tsv (generated from old step)
ontoTermsFile = open(sys.argv[1])
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()

#cuiMatchFile = open("cuiMatchTermsWoViews.tsv", "w+")
'''
ontoTermInfo = {}
for i in range(len(ontoTermLines)):
    if i == 0:
        continue
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    if (not ontoTermInfo.get(ontoTermParams[0].strip())) and len(ontoTermParams) > 4:
         print ontoTermParams[4].strip()
         ontoTermInfo[ontoTermParams[0].strip()] = ontoTermParams[4].strip()
         cuiMatchFile.write(ontoTermParams[0].strip() + "\t" + ontoTermParams[4].strip() + "\n")
'''
ontoTermInfo = {}
for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    ontoTermInfo[ontoTermParams[0]] = ontoTermParams[1]
    print ontoTermParams[1]


termOverlapFile = open(sys.argv[2])
overlappedTerms = termOverlapFile.readlines()
termOverlapFile.close()

termOverlapFileRef = open(sys.argv[3], "w+")

for i in range(len(overlappedTerms)):
    if i == 0:
       continue
    overlapTermParams = overlappedTerms[i].strip().split("\t")
    #overlapEnd = overlapTermParams[2].strip().split("http")
    #overlapOntologies = overlapEnd[0]
    #termPairsStr = "http" + "http".join(overlapEnd[1:len(overlapEnd)])
    termPairs = overlapTermParams[3].split(":-:")

    print termPairs
    if len(termPairs) > 1:
        baseCui = ontoTermInfo.get(termPairs[0])
        if baseCui:
            print baseCui
            toWrite = False
            cuiStr = baseCui
            for i in range(1, len(termPairs)):
                if ontoTermInfo.get(termPairs[i]):
                    cuiStr = cuiStr + ":-:" + ontoTermInfo[termPairs[i]]
                    if baseCui != ontoTermInfo[termPairs[i]]:
                        toWrite = True
                else:
                    cuiStr = cuiStr + ":-:" + "None"
                    toWrite = True
            if toWrite:
                termOverlapFileRef.write(overlapTermParams[0] + "\t" + overlapTermParams[1] + "\t" + overlapTermParams[2] + "\t" + overlapTermParams[3] + "\t" + cuiStr + "\n")
        else:
            termOverlapFileRef.write(overlapTermParams[0] + "\t" + overlapTermParams[1] + "\t" + overlapTermParams[2] + "\t" + overlapTermParams[3] + "\n")
        #termOverlapFileRef.write(overlapTermParams[0] + "\t" + overlapTermParams[1] + "\t" + overlapTermParams[2] + "\t" + overlapTermParams[3] + "\n")
        