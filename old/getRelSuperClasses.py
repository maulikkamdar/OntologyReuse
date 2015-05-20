import os
import sys
import numpy

relFile = open(sys.argv[1])
relLines = relFile.readlines()
relFile.close()
allRelatedTerms = {}
ontoSubclassFile = open(sys.argv[2])
ontoSubclassLines = ontoSubclassFile.readlines()
ontoSubclassFile.close()
ontoSubclasses = {}
ontoSuperClasses = {}
ontoSuperEdges = {}

outputNodes = []
outputNodesFile = open(sys.argv[3]+"_nodes.txt", "w+")
outputEdgesFile = open(sys.argv[3]+"_edges.txt", "w+")

def getSuperClasses(ontoTerm, isExists, maxDepth, baseTerm):
    # Too many base cases :/
    #print ontoSubclasses.get(ontoTerm)
    if ontoSuperClasses.get(ontoTerm):
        return ontoSuperClasses[ontoTerm]
    if not ontoSuperEdges.get(baseTerm):
        ontoSuperEdges[baseTerm] = []
    if maxDepth > 990:
        return isExists
    if ontoSubclasses.get(ontoTerm):
        if len(ontoSubclasses.get(ontoTerm)) == 0:
            return []
        else:
            superClasses = ontoSubclasses[ontoTerm]
            #print ontoTerm
            for i in ontoSubclasses[ontoTerm]:
                ontoSuperEdges[baseTerm].append(ontoTerm + "-->" + i)
                if not i in isExists:
                    obtSuperClasses = getSuperClasses(i, superClasses, maxDepth+1, baseTerm)
                    isExists = list(set(superClasses) | set(obtSuperClasses))
            ontoSuperClasses[ontoTerm] = isExists
            return isExists
    else:
        return []

# getSuperClasses("http://purl.obolibrary.org/obo/UBERON_0003623")
for i in range(len(ontoSubclassLines)):
    if i == 0:
        continue
    ontoSubclassParts = ontoSubclassLines[i].strip().split("\t")
    if len(ontoSubclassParts) > 4:
        curSubClass = ontoSubclassParts[4][0:len(ontoSubclassParts[4])-3].split(":-:")
        if ontoSubclasses.get(ontoSubclassParts[0]):
            extendPortion = []
            for k in curSubClass:
                if not k in ontoSubclasses[ontoSubclassParts[0]]:
                    extendPortion.append(k)
            ontoSubclasses[ontoSubclassParts[0]].extend(extendPortion)
        else:
            ontoSubclasses[ontoSubclassParts[0]] = curSubClass
    else:
        ontoSubclasses[ontoSubclassParts[0]] = []

for i in range(len(relLines)):
    relParams = relLines[i].split("\t")
    relatedTerm = relParams[0]
    allRelatedTerms[relatedTerm] = relParams[1]
    print relatedTerm
    relsuperClasses = getSuperClasses(relatedTerm, [relatedTerm], 0, relatedTerm)
    outputNodes.append(relatedTerm)
    outputNodes = list(set(outputNodes) | set(relsuperClasses))
    
    #print relatedTerm + "\n ------- \n" + "\n".join(relsuperClasses) + "\n" 

groups = {}
groupcnt = 1
for i in range(len(outputNodes)):
    if outputNodes[i] in allRelatedTerms:
        if not groups.get(allRelatedTerms[outputNodes[i]]):
            groups[allRelatedTerms[outputNodes[i]]] = groupcnt
            groupcnt = groupcnt+1
        outputNodesFile.write(outputNodes[i] + "\t" + str(groups[allRelatedTerms[outputNodes[i]]]) + "\n")
    else:
        outputNodesFile.write(outputNodes[i] + "\t100\n")

#outputFile.write("\n")

for i in ontoSuperEdges:
    for k in ontoSuperEdges[i]:
        outputEdgesFile.write(k + "\n")