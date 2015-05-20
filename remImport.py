import os
import sys
import numpy
import re

reuseImport = open(sys.argv[1])
reuseImportLines = reuseImport.readlines()
reuseImport.close()

newImport = open(sys.argv[4])
newImportLines = newImport.readlines()
newImport.close()

# cooccur File
ontoTermsFile = open(sys.argv[2])
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()

removedImport = open(sys.argv[3], "w+")
importOntologies = {}

for i in range(len(reuseImportLines)):
    reuseImportParams = reuseImportLines[i].strip().split("\t")
    if reuseImportParams[5] == "Import":
        # Because SPARQL uses nif and ontologies use NIFSTD
        if reuseImportParams[0].lower() == "nif":
            importTerm = "nifstd"
        elif reuseImportParams[0].lower() == "nif_dysfunction":
            importTerm = "nifdys"
        elif reuseImportParams[0].lower() == "nif_cell":
            importTerm = "nifcell"
        elif reuseImportParams[0].lower() == "nif-subcell":
            importTerm = "nifsubcell"
        else:
            importTerm = reuseImportParams[0].lower()

        if reuseImportParams[1].lower() == "nif":
            importingTerm = "nifstd"
        elif reuseImportParams[1].lower() == "nif_dysfunction":
            importingTerm = "nifdys"
        elif reuseImportParams[1].lower() == "nif_cell":
            importingTerm = "nifcell"
        elif reuseImportParams[1].lower() == "nif-subcell":
            importingTerm = "nifsubcell"
        else:
            importingTerm = reuseImportParams[1].lower()

        if importOntologies.get(importingTerm):
            importOntologies[importingTerm].append(importTerm)
        else:
            importOntologies[importingTerm] = [importTerm]

for i in range(len(newImportLines)):
    newImportParams = newImportLines[i].strip().split("\t")
    if newImportParams[5] == "Import":
        if importOntologies.get(newImportParams[1].lower()):
            importOntologies[newImportParams[1].lower()].append(newImportParams[0].lower())
        else:
            importOntologies[newImportParams[1].lower()] = [newImportParams[0].lower()]

#for key in importOntologies:
#    print key
#    print importOntologies[key]

for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    ontologies = ontoTermParams[3].strip().split(":-:")
    
    isImport = False
    for k in ontologies:
        if importOntologies.get(k.lower()):
            count = 1
            #print importOntologies[k.lower()]
            for m in ontologies:
                if m.lower() == k.lower():
                   continue
                if m.lower() in importOntologies[k.lower()]:
                    count = count + 1
            
            if count == int(ontoTermParams[2]):
                isImport = True
                #print ontoTermParams[0]
                break

    if not isImport:
       #print "Reuse - " + ontoTermParams[0]
       removedImport.write(ontoTermLines[i])
