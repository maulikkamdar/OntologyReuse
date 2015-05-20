import os
import sys

addImportStatsFile = open(sys.argv[1])
newImportStatsFile = open(sys.argv[2], "w+")

relations = addImportStatsFile.readlines()
for i in range(len(relations)):
    relationParams = relations[i].strip().split("\t")
    if relationParams[0] != relationParams[1]:
        imp1 = float(relationParams[2])/float(relationParams[3])
        imp2 = float(relationParams[2])/float(relationParams[4])
        if (imp1 > 0.35):
            newImportStatsFile.write(relationParams[1] + "\t" + relationParams[0] + "\t" + str(relationParams[2]) + "\t" + str(relationParams[3]) + "\t" + str(imp1) + "\tImport\n")
        if (imp2 > 0.35):
            newImportStatsFile.write(relationParams[0] + "\t" + relationParams[1] + "\t" + str(relationParams[2]) + "\t" + str(relationParams[4]) + "\t" + str(imp2) + "\tImport\n")
