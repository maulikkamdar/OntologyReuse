import os
import re

ontoTermsFile = open("ontoTermsWoClasses_1.tsv")
ontoTermsReFile = open("ontoTermsReWoClasses_1.tsv", "w+")
ontoTermsReFile.write("Term URI\tOntology\tTerm Label\tOntology URI\tTerm CUI\tTerm TUI\nSource Onto Naive\n")
ontoUniqueTermsFile =  open("ontoUniqueTermsWoClasses.tsv", "w+")

ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()

ontologiesAcrList = []
ontologyMapper = {}
noMap = 0
uniqueTerms = {}

for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        ontologiesAcrList.append(file.strip().split('--')[0].lower())
        ontologyMapper[file.strip().split('--')[0].lower()]= file.strip().split('--')[0]

for i in range(len(ontoTermLines)):
    ontologySubstr = []
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    mapping = ontoTermParams[0].strip().lower()
    mappingParts = re.split('[^0-9a-zA-Z]+', mapping)
    print mappingParts
    if not uniqueTerms.get(ontoTermParams[0].strip()):
        for j in ontologiesAcrList:
            if not j == ontoTermParams[1].lower() and j in mappingParts[:-1]:
                ontologySubstr.append(j)
            
        maxLen = 0
        ontology = ''
        for k in ontologySubstr:
            if len(k) > maxLen:
                maxLen = len(k)
                ontology = k
    
        if ontology == '':
            noMap = noMap + 1
        else:
            print ontologyMapper.get(ontology)
            uniqueTerms[ontoTermParams[0].strip()] = []
            uniqueTerms[ontoTermParams[0].strip()].append(ontologyMapper.get(ontology))
            uniqueTerms[ontoTermParams[0].strip()].append(1)
            uniqueTerms[ontoTermParams[0].strip()].append([])
            uniqueTerms[ontoTermParams[0].strip()][2].append(ontoTermParams[1].strip())
    else:
        uniqueTerms[ontoTermParams[0].strip()][1] = uniqueTerms[ontoTermParams[0].strip()][1]+1
        uniqueTerms[ontoTermParams[0].strip()][2].append(ontoTermParams[1].strip())

    if not ontology == '':
        ontoTermsReFile.write("\t".join(ontoTermParams) + "\t" + ontologyMapper.get(ontology) + "\n")
    else:
        ontoTermsReFile.write("\t".join(ontoTermParams) + "\t\n")

print noMap
print len(ontoTermLines)
print len(uniqueTerms)


#5698372
#7257890
#1193275

for uniqueTerm in uniqueTerms:
     ontoUniqueTermsFile.write(uniqueTerm + "\t" + uniqueTerms[uniqueTerm][0] + "\t" + str(uniqueTerms[uniqueTerm][1]) + "\t" + ":-:".join(uniqueTerms[uniqueTerm][2]) + "\n")