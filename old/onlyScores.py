import os
import sys
import numpy

ontoCoccurFile = open(sys.argv[1])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()

termCooccurMatrixFile = open(sys.argv[2], "w+")
#termCooccurMatrixLoc = open(sys.argv[3], "w+")


for i in range(len(ontoTermLines)):
    if i == 0:
       continue
    ontoPartsi = ontoTermLines[i].strip().split("\t")
    ontoPartsiOnto = ontoPartsi[3].strip().split(":-:")
    print i
    topScores = []
    
    countTracker = ""
    for j in range(len(ontoTermLines)):
        if j == 0 or i == j:
           continue
        else:
            ontoPartsj = ontoTermLines[j].strip().split("\t")
            ontoPartsjOnto = ontoPartsj[3].strip().split(":-:")
            #print ontoPartsiOnto
            #print ontoPartsjOnto
            #print list(set(ontoPartsiOnto) & set(ontoPartsjOnto))
            #print list(set(ontoPartsiOnto) | set(ontoPartsjOnto))
            count = round(float(len(list(set(ontoPartsiOnto) & set(ontoPartsjOnto))))/float(len(list(set(ontoPartsiOnto) | set(ontoPartsjOnto)))),2)
            #print count
            topScores.append({"rel": str(i) + "-" +  str(j), "count": count})
    
    finalTopScores = sorted(topScores, key=lambda k: k['count'], reverse=True)[0:int(sys.argv[3])]
    #print finalTopScores
    cooccurStr = ""
    locStr = ""

    for i in range(len(finalTopScores)):
        nodes = finalTopScores[i]["rel"].split("-")
        if finalTopScores[i]["count"] > 0.0:
            termCooccurMatrixFile.write(nodes[0] + "\t" + nodes[1] + "\t" + str(finalTopScores[i]["count"]) + "\n")
        #cooccurStr = cooccurStr + str(finalTopScores[i]["count"]) + "\t"
        #locStr = locStr + nodes[1] + "\t"
    
    #termCooccurMatrixFile.write(cooccurStr[0:len(cooccurStr)-2] + "\n")
    #termCooccurMatrixLoc.write(locStr[0:len(locStr)-2] + "\n")

    #if i > 2:
    #    break
termCooccurMatrixFile.close()