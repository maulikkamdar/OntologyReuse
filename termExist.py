import sys
import os

ontoTermsFile = open(sys.argv[1])
ontoTerms = {}
ontoCoccurFile = open(sys.argv[2], "w+")
ontoCoccurFile.write("Term URI\tLabel\tcount\tOntologies\n")

ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()

print len(ontoTermLines)
for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    mapping = ontoTermParams[0].strip()
    if ontoTerms.get(mapping):
        print "Term exists"
        ontoTerms[mapping][0] = ontoTerms[mapping][0]+1
        if ontoTerms[mapping][2] == "":
            ontoTerms[mapping][2] = ontoTermParams[2].strip()
    else:
        print mapping
        ontoTerms[mapping] = [1,[], ontoTermParams[2].strip()]
    ontoTerms[mapping][1].append(ontoTermParams[1].strip())

count = 0
for ontoTerm in ontoTerms:
    if ontoTerms[ontoTerm][0] > 1:
        count = count+1
        print ontoTerm + "\t" + ontoTerms[ontoTerm][2] + "\t" + str(ontoTerms[ontoTerm][0]) + "\t" + ":-:".join(ontoTerms[ontoTerm][1]) + "\n"
        ontoCoccurFile.write(ontoTerm + "\t" + ontoTerms[ontoTerm][2] + "\t" + str(ontoTerms[ontoTerm][0]) + "\t" + ":-:".join(ontoTerms[ontoTerm][1]) + "\n")

print count