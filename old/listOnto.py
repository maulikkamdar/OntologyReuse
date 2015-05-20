import os
import sys

listOntoFile = open("listOntoAll.tsv", "w+")

for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        listOntoFile.write(file.split("--")[0] + "\n")
     