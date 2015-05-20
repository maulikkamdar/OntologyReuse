import os
import sys

csvFile = open(sys.argv[1])
csvLines = csvFile.readlines()
csvFile.close()

mapperFile = open(sys.argv[2], "w+")

classIdentifier = 0 
legacyIdentifier = 0 
parentClassIdentifier = 0

for i in range(len(csvLines)):
    csvParams = csvLines[i].strip().split(",")
    mapperLine = ""
    if i == 0:
        for k in range(len(csvParams)):
            if csvParams[k] == "Class ID":
                classIdentifier = k
            if csvParams[k] == "Legacy_Concept_Name" and legacyIdentifier != 0:
                legacyIdentifier = k
            if csvParams[k] == "Parents":
                parentClassIdentifier = k
        continue
    for k in range(len(csvParams)):
        if k == classIdentifier:
            mapperLine = mapperLine + csvParams[k] + "\t"
            print csvParams[k]
        if k == parentClassIdentifier:
            mapperLine = mapperLine + csvParams[k] + "\t"
        if k == legacyIdentifier:
            mapperLine = mapperLine + csvParams[k] + "\n"

    mapperFile.write(mapperLine)


    
            