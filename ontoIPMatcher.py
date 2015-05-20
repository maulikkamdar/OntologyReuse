import os
import sys
import re


ontoFile = open(sys.argv[1])
ontoLines = ontoFile.readlines()
ontoFile.close()
ontoClasses = []

for k in range(len(ontoLines)):
    if k == 0:
        continue
    ontoParams = ontoLines[k].strip().split()
    ontoClass = ontoParams[0][1:len(ontoParams[0])-1]
    #print ontoClass
    if not ontoClass in ontoClasses:
        print ontoClass
        ontoClasses.append(ontoClass)
   

print "opening to read iplog" + sys.argv[2]

ipFile = open(sys.argv[2])
ipLines = ipFile.readlines()
print ipLines[0]
ipFile.close()
print "Read Lines"

containedFile = open(sys.argv[3], "w+")

for k in range(len(ipLines)):
    ipLineParts = ipLines[k].strip().split("\t")
    #print ipLineParts[0]
    if not "target=root" in ipLineParts[2]:
        if ipLineParts[2] in ontoClasses:
            containedFile.write(ipLineParts[2] + "\n")
        else:
            print ipLineParts[2]
            containedFile.write("\n")
    else:
        print ipLineParts[2]
        containedFile.write("\n")