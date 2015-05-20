import os
import sys
import re
# reduced file
xrefFile = open(sys.argv[1])
xrefLines = xrefFile.readlines()
xrefFile.close()

xrefStatisticsFile = open(sys.argv[2], "w+")
xrefFile = open("allXrefsWoViews.tsv", "w+")
notationFile = open("allNotationsWoViews.tsv", "w+")


uniqueTermsNotations = {}
uniqueTermXrefs = {}

xrefPairs = {}
totalXrefs = 0
for i in range(len(xrefLines)):
    xrefParams = xrefLines[i].strip().split("\t")
    #endTermParams = re.split(r'[/]', xrefParams[0].strip())
    #termId = endTermParams[len(endTermParams)-1]
    termOntologyParams = re.split('[^0-9a-zA-Z]+', xrefParams[0].strip())
    if "http://purl.obolibrary.org/obo/PR" in xrefParams[0].strip():
        termOntology = "-".join(termOntologyParams[0:len(termOntologyParams)-2])
    else:
        termOntology = "-".join(termOntologyParams[0:len(termOntologyParams)-1])
    if not uniqueTermsNotations.get(termOntology):
       #print xrefParams[0].strip()
       #print termOntology
       uniqueTermsNotations[termOntology] = 1
    else:
       uniqueTermsNotations[termOntology] = uniqueTermsNotations[termOntology] + 1
    #print termOntologyParams-1
    #if termOntologyParams[0] == "":
    #    continue
    #termOntology = termOntologyParams[0]
    xrefValues = xrefParams[2].strip().split(":-:")
    totalXrefs = totalXrefs + len(xrefValues)-1
    for k in range(len(xrefValues)):
        if xrefValues[k] == "":
            continue
        #tarOntologyParams = re.split('[^0-9a-zA-Z]+', xrefValues[k])
        tarOntologyParams = xrefValues[k].split(":")
        #print tarOntologyParams
        if len(tarOntologyParams) > 1:
            #tarOntology = "-".join(tarOntologyParams[0:len(tarOntologyParams)-1])
            tarOntology = re.sub('[^0-9a-zA-Z]+', '', tarOntologyParams[0])

            if tarOntology.lower() == "http" or tarOntology.lower() == "https":
                tarOntologyParams = re.split('[^0-9a-zA-Z]+', xrefValues[k])
                tarOntology = "-".join(tarOntologyParams[0:len(tarOntologyParams)-2])
                print tarOntology

            if not uniqueTermXrefs.get(tarOntology):
                uniqueTermXrefs[tarOntology] = 1
            else:
                uniqueTermXrefs[tarOntology] = uniqueTermXrefs[tarOntology] +1

            if xrefPairs.get(termOntology + ":-:" + tarOntology):
                xrefPairs[termOntology + ":-:" + tarOntology] = xrefPairs[termOntology + ":-:" + tarOntology] + 1
            else:
                #print termOntology + ":-:" + tarOntology
                xrefPairs[termOntology + ":-:" + tarOntology] = 1

print totalXrefs
#4429204

for pair in xrefPairs:
    pairParams = pair.split(":-:")
    xrefStatisticsFile.write(pairParams[0] + "\t" + pairParams[1] + "\t" + str(xrefPairs[pair]) + "\n")

for notation in uniqueTermsNotations:
    notationFile.write(notation + "\t" + str(uniqueTermsNotations[notation]) + "\n")

for xref in uniqueTermXrefs:
    xrefFile.write(xref + "\t" + str(uniqueTermXrefs[xref]) + "\n")
