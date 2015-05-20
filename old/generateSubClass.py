import os
import re
import sys

ontoTermsFile = open(sys.argv[1], "w+")

ontoTermsFile.write("Term URI\tOntology\tTerm Label\tOntology URI\tUMLSCUI\tUMLSTUI\tSubclassStr\n")
ontologyTerms = {}
previousTerm = ""
for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        ontoVersionFile = open(root + '/' + file)
        ontologyLines = ontoVersionFile.readlines()
        ontoVersionFile.close()
        print file
        for i in range(len(ontologyLines)):
            if i == 0:
                continue
            ontologyTriples = ontologyLines[i].strip().split()

            ontologyParts = re.split(r'[/#]',ontologyTriples[0].strip()[1:len(ontologyTriples[0])-1])

            if not ontologyTriples[0] == previousTerm:
                if not previousTerm == "":
                    if ontologyTerms[previousTerm]["type"] == "class":
                        ontoTermsFile.write(previousTerm[1:len(previousTerm)-1] + "\t" + ontologyTerms[previousTerm]["ontology"]+ "\t" + ontologyTerms[previousTerm]["termLabel"] + "\t" + ontologyTerms[previousTerm]["ontologyUri"] + "\t" + ontologyTerms[previousTerm]["termCui"] + "\t" + ontologyTerms[previousTerm]["termTui"] + "\t" + ontologyTerms[previousTerm]["subClassOf"] + "\n")
                        #print previousTerm
                    else:
                        print previousTerm
                previousTerm = ontologyTriples[0]
                ontologyIdentifier = file.strip().split("--")
                ontologyTerms[ontologyTriples[0]] = {"ontology":ontologyIdentifier[0], "ontologyUri": "http://data.bioontology.org/ontologies/"+ontologyIdentifier[0]+"/submissions/"+ontologyIdentifier[1], "type": "", "termLabel": "", "termCui": "", "termTui": "", "subClassOf": ""}
            predicateTerms = re.split(r'[/#]',ontologyTriples[1].strip()[1:len(ontologyTriples[1])-1])
            predicate = predicateTerms[len(predicateTerms)-1]
            if predicate == "subClassOf":
                ontologyTerms[ontologyTriples[0]]["subClassOf"] = ontologyTerms[ontologyTriples[0]]["subClassOf"] + ontologyTriples[2].strip()[1:len(ontologyTriples[2])-1] + ":-:"
            if predicate == "prefLabel" or predicate == "title" or predicate == "label":
                title = ' '.join(ontologyTriples[2:]).split("^^")[0]
                if "@en" in title.lower():
                    title = title[0:len(title)-5]
                ontologyTerms[ontologyTriples[0]]["termLabel"] = title[1:len(title)-1]
            if predicate == "cui":
                cui = ontologyTriples[2].strip().split("^^")[0]
                ontologyTerms[ontologyTriples[0]]["termCui"] = cui[1:len(cui)-1]
            if predicate == "tui":
                tui = ontologyTriples[2].strip().split("^^")[0]
                ontologyTerms[ontologyTriples[0]]["termTui"] = tui[1:len(tui)-1]
            if predicate == "type":
                termtypeParams = re.split(r'[/#]',ontologyTriples[2].strip()[1:len(ontologyTriples[2])-1])
                termType = termtypeParams[len(termtypeParams)-1].lower()
                ontologyTerms[ontologyTriples[0]]["type"] = termType
                
            