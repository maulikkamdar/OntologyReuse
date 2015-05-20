import os
import sys
import re

ontoTermsFile = open(sys.argv[1])
ontoTerms = ontoTermsFile.readlines()
ontoTermsFile.close()

umlsCoocurFile = open(sys.argv[2], "w+")
umlsUis = {}
umlsUisSource = {}

for i in range(len(ontoTerms)):
    if i == 0:
        continue
    ontoTermParams = ontoTerms[i].strip().split("\t")
    if len(ontoTermParams) > 4:
        cui = ontoTermParams[4].strip() # Change this to 5 for TUI
        #print cui
        shortTerms = re.split(r'[/#]',ontoTermParams[0].strip())
        specId = shortTerms[len(shortTerms)-1]
        #print specId
        if umlsUis.get(cui):
            if not ontoTermParams[1] in umlsUis[cui]:
                umlsUis[cui].append(ontoTermParams[1])
        else:
            umlsUis[cui] = [ontoTermParams[1]]

        if specId.lower() == cui.lower():
            if umlsUisSource.get(cui):
                if not ontoTermParams[1] in umlsUisSource[cui]:
                    umlsUisSource[cui].append(ontoTermParams[1])
            else:
                umlsUisSource[cui] = [ontoTermParams[1]]
                #print umlsUisSource[cui]

for cui in umlsUis:
    if len(umlsUis[cui]) > 1:
        if not umlsUisSource.get(cui):
            umlsCoocurFile.write(cui +  "\t" + ":-:".join(umlsUis[cui]) + "\n")
        else:
            umlsCoocurFile.write(cui +  "\t" + ":-:".join(umlsUis[cui]) + "\t" + umlsUisSource[cui][0] + "\n")

         
