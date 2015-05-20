import os
import sys
import numpy

sys.setrecursionlimit(10000)
ontoCoccurFile = open(sys.argv[1])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()

ontoSubclassFile = open(sys.argv[3])
ontoSubclassLines = ontoSubclassFile.readlines()
ontoSubclassFile.close()
ontoSubclasses = {}

# The weights
w1 = float(sys.argv[4])
w2 = float(sys.argv[5])

ontoSuperClasses = {}

def getSuperClasses(ontoTerm, isExists, maxDepth):
    # Too many base cases :/
    #print ontoSubclasses.get(ontoTerm)
    if ontoSuperClasses.get(ontoTerm):
        return ontoSuperClasses[ontoTerm]
    if maxDepth > 990:
       return isExists
    if ontoSubclasses.get(ontoTerm):
        if len(ontoSubclasses.get(ontoTerm)) == 0:
            return []
        else:
            superClasses = ontoSubclasses[ontoTerm]
            #print ontoTerm
            for i in ontoSubclasses[ontoTerm]:
                if not i in isExists:
                    obtSuperClasses = getSuperClasses(i, superClasses, maxDepth+1)
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

termCooccurMatrixFile = open(sys.argv[2], "w+")
dNu = 1

for i in range(len(ontoTermLines)):
    ontoPartsi = ontoTermLines[i].strip().split("\t")
    ontoPartsiOnto = ontoPartsi[3].strip().split(":-:")
    print i
    topScores = []
    
    countTracker = ""
    for j in range(len(ontoTermLines)):
        if i == j:
            termCooccurMatrixFile.write(str(i) + "\t" + str(j) + "\t" + str(1) + "\t" + str(1) + "\n")
        else:
            ontoPartsj = ontoTermLines[j].strip().split("\t")
            ontoPartsjOnto = ontoPartsj[3].strip().split(":-:")
            commonOnto = list(set(ontoPartsiOnto) & set(ontoPartsjOnto))
            count = round(float(len(commonOnto))/float(len(list(set(ontoPartsiOnto) | set(ontoPartsjOnto)))),2)

            if len(commonOnto) > 0: # If they have the same common ontologies shared or assume 0
                ontopartsisuper = getSuperClasses(ontoPartsi[0].strip(), [ontoPartsi[0].strip()], 0)
                ontopartsjsuper = getSuperClasses(ontoPartsj[0].strip(), [ontoPartsj[0].strip()], 0)
                unionCount = len(list(set(ontopartsisuper) | set(ontopartsjsuper)))
                if unionCount > 0:
                    sem_count = round(float(len(list(set(ontopartsisuper) & set(ontopartsjsuper))))/float(unionCount),2)
                else:
                    sem_count = 0
            else:
                sem_count = 0
            combcount = w1*count + w2*sem_count
            print combcount
            if combcount > float(sys.argv[6]):
                termCooccurMatrixFile.write(str(i) + "\t" + str(j) + "\t" + str(count) + "\t" + str(sem_count) + "\n")
            
termCooccurMatrixFile.close()


# 1 - Cooccurence File
# 2 - Output File Patterns
# 3 - Sublcass File
# 4 - Weight 1
# 5 - Weight 2
# 6 - Threshold
