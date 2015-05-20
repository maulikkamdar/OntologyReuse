# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import re


#Input
# Ontology Cooccur FIle
# Output - ontology list file
# Nonmapped- terms
# OntoSource File

ontoCoccurFile = open(sys.argv[1])
ontoTermLines = ontoCoccurFile.readlines()
ontoListile = open(sys.argv[2], "w+")
nomappedFile = open(sys.argv[3], "w+")
ontoSourceFile = open(sys.argv[4], "w+")

ontologiesAcrList = []
ontologyMapper = {}
noMap = 0
uniqueOntologies = []
noMapTerms = []

for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        ontoid = file.strip().split('--')[0]
        ontologiesAcrList.append(ontoid.lower())
        ontologyMapper[ontoid.lower()]= ontoid

for i in range(len(ontoTermLines)):
    if i == 0:
        continue
    ontologySubstr = []
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    mapping = ontoTermParams[0].strip().lower()
    sharedOntologies = ontoTermParams[3].strip().split(":-:")
    #print mapping
    mappingParts = re.split('[^0-9a-zA-Z]+', mapping)

    doesExist = False
    for share in sharedOntologies:
        if share.lower() in mappingParts:
            doesExist = True
            ontologySubstr.append(share)

    if not doesExist:
        for share in sharedOntologies:
            sharedParts = re.split('[^0-9a-zA-Z]+', share)
            for part in sharedParts:
                if part.lower() in mappingParts:
                    doesExist = True
                    ontologySubstr.append(share)

    if not doesExist:
        doesExist = True
        if "BiomedicalResourceOntology".lower() in mapping:
            ontologySubstr.append("BRO")
        elif "ncicb.nci.nih.gov" in mapping:
            ontologySubstr.append("NCIT")
        elif "ontoneurolog" in mapping:
            ontologySubstr.append("ONL-MSA")
        elif "birnlex" in mapping:
            ontologySubstr.append("BIRNLEX")
        elif "nif-subcellular" in mapping:
            ontologySubstr.append("NIFSUBCELL")
        elif "nif-cell" in mapping:
            ontologySubstr.append("NIFCELL")
        elif "nif-dysfunction" in mapping:
            ontologySubstr.append("NIFDYS")
        elif "ncbigene" in mapping:
            ontologySubstr.append("NCBIGENE")
        elif "biotop" in mapping:
            ontologySubstr.append("BT")
        elif "uniprot" in mapping:
            ontologySubstr.append("UniProt")
        elif "nbo" in mapping:
            ontologySubstr.append("NBO")
        elif "biopax" in mapping:
            ontologySubstr.append("BP")
        elif "mouse.brain-map.org" in mapping:
            ontologySubstr.append("ABA-AMB")
        elif "mthmst" in mapping:
            ontologySubstr.append("MTHMST")
        elif "geneontology" in mapping:
            ontologySubstr.append("GO")
        elif "researcharea" in mapping:
            ontologySubstr.append("BRO")
        elif "mgedontology" in mapping:
            ontologySubstr.append("MO")
        elif "bibo" in mapping:
            ontologySubstr.append("bibliographic")
        elif "http://purl.org/dc/" in mapping:
            ontologySubstr.append("DC")
        elif "http://example.org/testing.owl" in mapping:
            ontologySubstr.append("SNMD_BC")
        elif "http://purl.org/cpr/" in mapping:
            ontologySubstr.append("CPRO")
        elif "http://ontology.neuinfo.org/nif/backend" in mapping:
            ontologySubstr.append("NIFSTD")
        elif "icd" in mapping:
            ontologySubstr.append("ICD9CM")
        else:
            #print mapping
            doesExist = False

    if not doesExist:
        #print mapping
        for j in ontologyMapper:
            #print j
            if j in mapping:
                doesExist = True
                print ontologyMapper[j]
                ontologySubstr.append(ontologyMapper[j])

    if not doesExist:
        doesExist = True
        if "id" in mapping:
            ontologySubstr.append("IDQA")
        elif "mi" in mapping:
            ontologySubstr.append("PSI-MI")
        else:
            doesExist = False
            ontoSourceFile.write(ontoTermLines[i].strip() + "\t na \n")
            noMap = noMap + 1
            nomappedFile.write(mapping + "\n")

    if doesExist:
        maxLen = 0
        ontology = ''
        for k in ontologySubstr:
            if len(k) > maxLen:
                maxLen = len(k)
                ontology = k
        ontoSourceFile.write(ontoTermLines[i].strip() + "\t" + ontology + "\n")
        #print ontology
        if not ontology in uniqueOntologies:
            uniqueOntologies.append(ontology)


print noMap

for i in uniqueOntologies:
    ontoListile.write(i + "\n")
   
    