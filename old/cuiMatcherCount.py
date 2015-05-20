import os
import sys
import re

ontoTermsFile = open(sys.argv[1])
ontoTerms = ontoTermsFile.readlines()
ontoTermsFile.close()

umlsUis = {}
umlsUisSource = {}

ontoCooccurFile = open(sys.argv[2])
ontoCooccurs = [x.strip().split("\t")[0] for x in ontoCooccurFile.readlines()]
ontoCooccurFile.close()


for i in range(len(ontoTerms)):
    if i == 0:
        continue
    ontoTermParams = ontoTerms[i].strip().split("\t")
    if ontoTermParams[0] in ontoCooccurs:
        continue
    if len(ontoTermParams) > 4:
        cui = ontoTermParams[4].strip() # Change this to 5 for TUI
        print cui
        shortTerms = re.split(r'[/#]',ontoTermParams[0].strip())
 
        if umlsUis.get(cui):
            if not ontoTermParams[1] in umlsUis[cui]:
                umlsUis[cui].append(ontoTermParams[1])
        else:
            umlsUis[cui] = [ontoTermParams[1]]
    else:
        print i

cuiCount = 0
for cui in umlsUis:
    if len(umlsUis[cui]) > 1:
        cuiCount = cuiCount + len(umlsUis[cui])

print cuiCount
         
