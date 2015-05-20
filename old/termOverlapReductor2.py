import os
import re
import sys

termOverlapFile = open(sys.argv[1])
overlappedTerms = termOverlapFile.readlines()
termOverlapFile.close()

termOverlapFileRef = open(sys.argv[2], "w+")
for i in range(len(overlappedTerms)):
    overlappedTermsParams = overlappedTerms[i].strip().split("\t")
    termLines = overlappedTermsParams[3].strip().split(":-:")
    cuiParams = []
    if len(overlappedTermsParams) > 4:
        cuiParams = overlappedTermsParams[4].strip().split(":-:")

    match = True
    mainId = ""
    for k in range(len(termLines)):      
        if "ihtsdo.org/snomedct" in termLines[k].lower():
            continue      
        termLineParams = re.split('[^0-9a-zA-Z]+', termLines[k])
        prevMainId = mainId
        mainId = termLineParams[len(termLineParams)-1].lower()
        print mainId
        if k > 0 and len(cuiParams) > 0:
            if prevMainId != mainId and cuiParams[k] != cuiParams[k-1]:
                match = False
                break
        '''if k > 0 and len(cuiParams) == 0:
            if prevMainId != mainId:
                match = False
                break
        if k > 0 and len(cuiParams) > 0:
            if prevMainId != mainId and cuiParams[k] != cuiParams[k-1]:
                match = False
                break'''
        
    if not match:
        termOverlapFileRef.write(overlappedTerms[i])