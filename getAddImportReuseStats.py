import sys

#python getAddImportReuseStats.py ../Final\ Statistics/reuseImport.tsv ontocooccurWoViews.tsv ontoTermsWoviews.tsv
reuseImport = open(sys.argv[1])
reuseImportLines = reuseImport.readlines()
reuseImport.close()

# ontococcur file
ontoTermsFile = open(sys.argv[2])
ontoTermLines = ontoTermsFile.readlines()
ontoTermsFile.close()

#onto Terms file
allClassesFile = open(sys.argv[3])
allClassesLine = allClassesFile.readlines()
allClassesFile.close()

allClasses = {}
for i in range(len(allClassesLine)):
    allClassesParam = allClassesLine[i].strip().split("\t")
    if allClasses.get(allClassesParam[1]):
        allClasses[allClassesParam[1]].append(allClassesParam[0])
    else:
        print allClassesParam[1]
        allClasses[allClassesParam[1]] = [allClassesParam[0]]


ontoExists = []
ontoPairs = {}
#ontoPairsFile = open("ontoPairsWoUMLS.tsv", "w+")
addImportStatsFile = open("newImportStatsWoViews.tsv", "w+")
ontoCommon = {}

for i in range(len(reuseImportLines)):
    reuseImportParams = reuseImportLines[i].strip().split("\t")
    if reuseImportParams[5] == "Import":
        # Because SPARQL uses nif and ontologies use NIFSTD
        if reuseImportParams[0].lower() == "nif":
            importTerm = "nifstd"
        elif reuseImportParams[0].lower() == "nif_dysfunction":
            importTerm = "nifdys"
        elif reuseImportParams[0].lower() == "nif_cell":
            importTerm = "nifcell"
        elif reuseImportParams[0].lower() == "nif-subcell":
            importTerm = "nifsubcell"
        else:
            importTerm = reuseImportParams[0].lower()

        if reuseImportParams[1].lower() == "nif":
            importingTerm = "nifstd"
        elif reuseImportParams[1].lower() == "nif_dysfunction":
            importingTerm = "nifdys"
        elif reuseImportParams[1].lower() == "nif_cell":
            importingTerm = "nifcell"
        elif reuseImportParams[1].lower() == "nif-subcell":
            importingTerm = "nifsubcell"
        else:
            importingTerm = reuseImportParams[1].lower()

        if not importTerm in ontoExists:
            ontoExists.append(importTerm)
        if not importingTerm in ontoExists:
            ontoExists.append(importingTerm)    


for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    if ontoPairs.get(ontoTermParams[3]):
        ontoPairs[ontoTermParams[3]] = ontoPairs[ontoTermParams[3]] + 1
    else:
        ontoPairs[ontoTermParams[3]] = 1

for pair in ontoPairs:
    ontologies = pair.strip().split(":-:")
    for i in ontologies:
        if not i.lower() in ontoExists:
            for k in ontologies:
                share = 0
                if not (ontoCommon.get(i + ":-:" + k) or ontoCommon.get(k + ":-:" + i)):
                    if allClasses.get(i) and allClasses.get(k):
                        share = len(list(set(allClasses.get(i)) & set(allClasses.get(k))))
                        ontoCommon[i + ":-:" + k] = share
                        print i + ":-:" + k + "\t" + str(share)
                    else:
                        print i + ":-:" + k

for pair in ontoCommon:
    ontos = pair.strip().split(":-:")
    print ontos[0] + "\t" + ontos[1] + "\t" + str(ontoCommon[pair]) + "\t" + str(len(allClasses.get(ontos[0]))) + "\t" + str(len(allClasses.get(ontos[1])))
    addImportStatsFile.write(ontos[0] + "\t" + ontos[1] + "\t" + str(ontoCommon[pair]) + "\t" + str(len(allClasses.get(ontos[0]))) + "\t" + str(len(allClasses.get(ontos[1]))) + "\n")

