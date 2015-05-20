import os
import sys
import numpy

userFile = open(sys.argv[1])
w1 = float(sys.argv[2])
w2 = float(sys.argv[3])
ontoCoccurFile = open(sys.argv[4])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()
outputFile = sys.argv[5]

userTerms = userFile.readlines()
userFile.close()
ontoTermLocator = {}

for i in range(len(ontoTermLines)):
    if i == 0:
        continue
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    ontoTermLocator[ontoTermParams[0]] = i

scoreMatrix = numpy.zeros([len(userTerms), len(ontoTermLines)-1], dtype=float)
baseMatrix = numpy.zeros([len(userTerms), len(ontoTermLines)-1], dtype=float)

for i in range(len(userTerms)):
    print i
    userTermParams = userTerms[i].strip().split("\t")
    userTerm = userTermParams[0]
    termNumber = ontoTermLocator.get(userTerm)
    if not termNumber:
        print "Term is not re-used in any ontologies"
    # Random blob because we have batch files
    fileNumber = int(termNumber/1500)+1
    scoreFile = open(outputFile + "_" + str(fileNumber) + ".tsv")
    scoreLines = scoreFile.readlines()
    scoreFile.close()
    for j in range(len(scoreLines)):
        scoreParams = scoreLines[j].strip().split("\t")
        if int(scoreParams[0]) == termNumber:
            baseMatrix[i][int(scoreParams[1])-1] = w1*float(scoreParams[2]) + w2*float(scoreParams[3])
            #print baseMatrix[i][int(scoreParams[1])-1]
            scoreMatrix[i][int(scoreParams[1])-1] = int(userTermParams[1])*(baseMatrix[i][int(scoreParams[1])-1])
        

scoreSum = numpy.sum(scoreMatrix, axis=0)
baseSum = numpy.sum(baseMatrix, axis=0)
filterVal = numpy.divide(scoreSum, baseSum) 

relatedTerms = []
for i in ontoTermLocator:
    if not numpy.isnan(filterVal[ontoTermLocator[i]-1]):
        relatedTerms.append({"term": i, "value": filterVal[ontoTermLocator[i]-1]})

sortedVals = sorted(relatedTerms, key=lambda k: k['value'], reverse=True)[0:100]
for i in range(len(sortedVals)):
    print sortedVals[i]['term'] + "\t" + str(sortedVals[i]['value'])  
#print sorted(filterVal, reverse=True)[0:10]       