import os
import re
import sys

ontoXrefTypeFile = open(sys.argv[1], "w+")
ontologyXrefs = {}

for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        ontoVersionFile = open(root + '/' + file)
        ontologyLines = ontoVersionFile.readlines()
        ontoVersionFile.close()
        print file
        ontologyId = file.strip().split("--")[0]
        for i in range(len(ontologyLines)):
            if i == 0:
                continue
            ontologyTriples = ontologyLines[i].strip().split()
            predicateTerms = re.split(r'[/#]',ontologyTriples[1].strip()[1:len(ontologyTriples[1])-1])
            predicate = predicateTerms[len(predicateTerms)-1]
            if "xref" in ontologyTriples[0].lower():
                sId = ontologyId + "--subject--" + ontologyTriples[0]
                print sId
                if not ontologyXrefs.get(sId):
                    ontologyXrefs[sId] = {"ontology": ontologyId, "type": "subject", "name": ontologyTriples[0], "exampleTriple": ontologyLines[i]}
            if "xref" in ontologyTriples[1].lower() and predicate != "hasDbXref":
                pId = ontologyId  + "--predicate--" + ontologyTriples[1]
                print pId
                if not ontologyXrefs.get(pId):
                    ontologyXrefs[pId] = {"ontology":ontologyId, "type": "predicate", "name": ontologyTriples[1], "exampleTriple": ontologyLines[i]}
            if "xref" in ontologyTriples[2].lower():
                oId = ontologyId  + "--object--" + ontologyTriples[2]
                print oId
                if not ontologyXrefs.get(oId):
                    ontologyXrefs[oId] = {"ontology":ontologyId, "type": "object", "name": ontologyTriples[2], "exampleTriple": ontologyLines[i]}

for xref in ontologyXrefs:
    ontoXrefTypeFile.write(ontologyXrefs[xref]["ontology"] + "\t" + ontologyXrefs[xref]["type"] + "\t" + ontologyXrefs[xref]["name"] + "\t" + ontologyXrefs[xref]["exampleTriple"] + "\n")
