import os
import re

ontoTermsFile = open("ontoTermsXrefsWoViews.tsv", "w+")
ontoTermsFile.write("Term URI\tOntology\tXref\n")
ontologyTerms = {}
previousTerm = ""
ontoListFile = open("ontologyRest.tsv")
ontoList = [x.strip().split("\t")[0] for x in ontoListFile.readlines()]

for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        if not file.split("--")[0] in ontoList:
            print file
            continue
        ontoVersionFile = open(root + '/' + file)
        ontologyLines = ontoVersionFile.readlines()
        ontoVersionFile.close()
        print file
        for i in range(len(ontologyLines)):
            if i == 0:
                continue
            ontologyTriples = ontologyLines[i].strip().split()
            if not ontologyTriples[0] == previousTerm:
                if not previousTerm == "":
                    if ontologyTerms[previousTerm]["type"] == "class" and ontologyTerms[previousTerm]["xref"] != "":
                        ontoTermsFile.write(previousTerm[1:len(previousTerm)-1] + "\t" + ontologyTerms[previousTerm]["ontology"]+ "\t" + ontologyTerms[previousTerm]["xref"] + "\t" + ontologyTerms[previousTerm]["predxref"] + "\n")
                        #print previousTerm
                    #else:
                    #    print previousTerm
                previousTerm = ontologyTriples[0]
                ontologyIdentifier = file.strip().split("--")
                ontologyTerms[ontologyTriples[0]] = {"ontology":ontologyIdentifier[0], "type": "", "xref": "", "predxref": ""}
            predicateTerms = re.split(r'[/#]',ontologyTriples[1].strip()[1:len(ontologyTriples[1])-1])
            predicate = predicateTerms[len(predicateTerms)-1]
            if "xref" in predicate.lower():
                xref = ontologyTriples[2].split("^^")[0]
                print xref
                #if "@en" in xref.lower():
                #    xref = xref[0:len(xref)-5]
                ontologyTerms[ontologyTriples[0]]["xref"] = ontologyTerms[ontologyTriples[0]]["xref"] + xref + ":-:"
                ontologyTerms[ontologyTriples[0]]["predxref"] = ontologyTerms[ontologyTriples[0]]["predxref"] + predicate + ":-:"
            if predicate == "type":
                termtypeParams = re.split(r'[/#]',ontologyTriples[2].strip()[1:len(ontologyTriples[2])-1])
                termType = termtypeParams[len(termtypeParams)-1].lower()
                ontologyTerms[ontologyTriples[0]]["type"] = termType
                