import os
import sys
import re

#python xrefProportion.py xrefReduced_main.tsv termcounts.tsv selectedXrefs.tsv selectedNotations.tsv
# reduced file
xrefFile = open(sys.argv[1])
xrefLines = xrefFile.readlines()
xrefFile.close()

termCountsFile = open(sys.argv[2])
termCountsLine = termCountsFile.readlines()
termCountsFile.close()
termCounts = {}

for i in range(len(termCountsLine)):
    termCountParams = termCountsLine[i].strip().split("\t")
    termCounts[termCountParams[0]] = int(termCountParams[1]) 


# selected xref File
inSelFile = open(sys.argv[3])
inSelLines = inSelFile.readlines()
inSelFile.close()
xrefRegex = {}

# selected Notation File
outSelFile = open(sys.argv[4])
outSelLines = outSelFile.readlines()
outSelFile.close()
notationRegex = {}

for i in range(len(inSelLines)):
    inSelParams = inSelLines[i].strip().split("\t")
    xrefRegex[inSelParams[0]] = inSelParams[2]

for i in range(len(outSelLines)):
    outSelParams = outSelLines[i].strip().split("\t")
    notationRegex[outSelParams[0]] = outSelParams[2]

# To Print 
inComingXrefs = {}
outgoingXrefs = {}

# To Keep Track for duplicates
inComingTerms = {}
outGoingTerms = {}
pairs = {}


outFile = open("outgoingXrefs.tsv", "w+")
inFile = open("incomingXrefs.tsv", "w+")
pairFile = open("pairFile.tsv", "w+")

uniqueTermsNotations = {}
uniqueTermXrefs = {}



for i in range(len(xrefLines)):
    xrefParams = xrefLines[i].strip().split("\t")
    termOntologyParams = re.split('[^0-9a-zA-Z]+', xrefParams[0].strip())
    if "http://purl.obolibrary.org/obo/PR" in xrefParams[0].strip():
        termOntology = "-".join(termOntologyParams[0:len(termOntologyParams)-2])
    else:
        termOntology = "-".join(termOntologyParams[0:len(termOntologyParams)-1])
   
    if notationRegex.get(termOntology) and not outGoingTerms.get(xrefParams[0].strip()):
        xrefValues = xrefParams[2].strip().split(":-:")
        print notationRegex.get(termOntology)
        count = 0
        for k in range(len(xrefValues)):
            if xrefValues[k] == "":
                continue
            tarOntologyParams = xrefValues[k].split(":")
            if len(tarOntologyParams) > 1:
                tarOntology = re.sub('[^0-9a-zA-Z]+', '', tarOntologyParams[0])

                inComingOnto = ""
                if tarOntology.lower() == "http" or tarOntology.lower() == "https":
                    tarOntologyParams = re.split('[^0-9a-zA-Z]+', xrefValues[k])
                    tarOntology = "-".join(tarOntologyParams[0:len(tarOntologyParams)-2])
                    for regXPattern in xrefRegex:
                        if regXPattern in tarOntology:
                            inComingOnto = xrefRegex[regXPattern]
                            break
                else:
                    if xrefRegex.get(tarOntology):
                        inComingOnto = xrefRegex[tarOntology]

                if inComingOnto == "":
                    continue
                else:
                    print inComingOnto
                    count = count + 1
                    if not inComingTerms.get(xrefValues[k]):
                        if inComingXrefs.get(inComingOnto):
                            inComingXrefs[inComingOnto] = inComingXrefs[inComingOnto] + 1
                        else:
                            inComingXrefs[inComingOnto] = 1
                    if pairs.get(notationRegex[termOntology] + ":-:" + inComingOnto):
                        pairs[notationRegex[termOntology] + ":-:" + inComingOnto] = pairs[notationRegex[termOntology] + ":-:" + inComingOnto] + 1
                    else:
                        pairs[notationRegex[termOntology] + ":-:" + inComingOnto] = 1
        
        if count > 0:       
            if outgoingXrefs.get(notationRegex[termOntology]):
                outgoingXrefs[notationRegex[termOntology]] = outgoingXrefs[notationRegex[termOntology]] + 1
            else:
                outgoingXrefs[notationRegex[termOntology]] = 1


for outOnto in outgoingXrefs:
    print outOnto
    if termCounts.get(outOnto):
        outFile.write(outOnto + "\t" + str(outgoingXrefs[outOnto]) + "\t" + str(termCounts[outOnto]) + "\n")
    else:
        outFile.write(outOnto + "\t" + str(outgoingXrefs[outOnto]) + "\tNone\n")

for inOnto in inComingXrefs:
    print inOnto
    if termCounts.get(inOnto):
        inFile.write(inOnto + "\t" + str(inComingXrefs[inOnto]) + "\t" + str(termCounts[inOnto]) + "\n")
    else:
        inFile.write(inOnto + "\t" + str(inComingXrefs[inOnto]) + "\tNone\n")


for pair in pairs:
    print pair
    pairFile.write(pair.split(":-:")[0] + "\t" + pair.split(":-:")[1] + "\t" + str(pairs[pair]) + "\n")