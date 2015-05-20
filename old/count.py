import sys
import os

ontoTermsFile = open("ontocooccurWoClassesWoUMLS.tsv")
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()
print len(ontoTermLines)

ontoTermsFile = open("ontocooccurWoClasses_1.tsv")
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()
print len(ontoTermLines)