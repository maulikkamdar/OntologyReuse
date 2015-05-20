import os
import sys
import datetime
import time
import urllib
import re

sourceDir = u"ConIPlogWoSub/"
outputFile = open("patterns.tsv", "w+")

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        ipFile = open(sourceDir + file)
        print file
        ipLines = ipFile.readlines()
        ipFile.close()
        for k in range(len(ipLines)):
            ipLineParts = ipLines[k].strip().split("\t")
            if "target=root" in ipLineParts[2]:
                outputFile.write(ipLineParts[2] + "\n")
                if k < len(ipLines)-1:
                    nextLineParts = ipLines[k+1].strip().split("\t")
                    outputFile.write(nextLineParts[2] + "\n")
          
          
               