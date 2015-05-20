import os
import sys


xrefFile = open(sys.argv[1])
xrefLines = xrefFile.readlines()
xrefFile.close()

xrefReducedFile = open(sys.argv[2], "w+")

xrefTerms = {}

for i in range(len(xrefLines)):
    if i == 0:
        continue
    xrefParams = xrefLines[i].strip().split("\t")
    if not xrefTerms.get(xrefParams[0].strip()):
        print xrefParams[0]
        xrefTerms[xrefParams[0].strip()] = {"count": 1, "xrefValues": xrefParams[2], "xrefTypes": xrefParams[3]}
    else:
        xrefTerms[xrefParams[0].strip()]["count"] = xrefTerms[xrefParams[0].strip()]["count"] + 1
    '''xrefTypes = xrefParams[3].strip().split(":-:")
    xrefValues = xrefParams[2].strip().split(":-:")
    for k in range(len(xrefTypes)):
        if xrefTypes[k] != "" and xrefTypes[k].lower() != "hasdbxref":
            print xrefTypes[k]
            xrefReducedFile.write(xrefParams[0] + "\t" + xrefParams[1] + "\t" + xrefTypes[k] + "\t" + xrefValues[k] + "\n")'''

for xref in xrefTerms:
    xrefReducedFile.write(xref + "\t" + str(xrefTerms[xref]["count"]) + "\t" + xrefTerms[xref]["xrefValues"] + "\t" + xrefTerms[xref]["xrefTypes"] + "\n")


    