import os
import sys
import numpy
import re

termsFile = open(sys.argv[2])
terms = termsFile.readlines()
termsFile.close()

termSimSimMatrix = open(sys.argv[3], "w+")
previousTerm = ""

superClasses = {}
simSimPairs = {}

def getEntirePath(term):
    nodeTerm = term
    while True:
        pass           

def generateSimSimMatrix():
    for i in range(len(terms)):
        for j in range(len(terms)):
            
            

for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        if file.strip().split('--')[0] == sys.argv[1]:
            ontoVersionFile = open(root + '/' + file)
            ontologyLines = ontoVersionFile.readlines()
            ontoVersionFile.close()
            for i in range(len(ontologyLines)):
                if i == 0:
                    continue
                ontologyTriples = ontologyLines[i].strip().split()
                predicateTerms = re.split(r'[/#]',ontologyTriples[1].strip()[1:len(ontologyTriples[1])-1])
                predicate = predicateTerms[len(predicateTerms)-1]
                if predicate == "subClassOf":
                    print "here"
                    if superClasses.get(ontologyTriples[0].strip()[1:len(ontologyTriples[0])-1]):
                        superClasses[ontologyTriples[0].strip()[1:len(ontologyTriples[0])-1]].append(ontologyTriples[2].strip()[1:len(ontologyTriples[2])-1])
                    else:
                        superClasses[ontologyTriples[0].strip()[1:len(ontologyTriples[0])-1]] = [ontologyTriples[2].strip()[1:len(ontologyTriples[2])-1]]
            generateSimSimMatrix()
            break

#for key in superClasses:
#    print key 
#    print superClasses[key]