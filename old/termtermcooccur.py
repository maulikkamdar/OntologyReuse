import os
import sys

ontoCooccurTermFile = open("ontocooccur1.tsv")
termTermCoocurFile = open("termtermcooccur.tsv", "w+")
termTermCoocurFile.write("Term1\tTerm2\tCooccurCount\tStatCooccur\tCooccurOntologies\n")
cooccurTermLines = ontoCooccurTermFile.readlines()

for i in range(len(cooccurTermLines)):
    if i == 0:
        continue
    for j in range(len(cooccurTermLines)):
        if j == 0:
            continue
        cooccurCount = 0
        cooccurOntos = []
        cooccurTermParams1 = cooccurTermLines[i].strip().split("\t")
        cooccurTermParams2 = cooccurTermLines[j].strip().split("\t")
        cooccurTermParams1Ontos = cooccurTermParams1[3].strip().split(":-:")
        cooccurTermParams2Ontos = cooccurTermParams2[3].strip().split(":-:")
        for k in cooccurTermParams1Ontos:
            if k in cooccurTermParams2Ontos:
                cooccurCount = cooccurCount + 1
                cooccurOntos.append(k)
        statCooccur = float(cooccurCount)/(float(cooccurTermParams1[2])+float(cooccurTermParams2[2])-float(cooccurCount))
        #print cooccurTermParams1[0]+"\t"+cooccurTermParams2[0]+"\t"+str(cooccurCount)+"\t"+str(statCooccur)
        termTermCoocurFile.write(cooccurTermParams1[0]+"\t"+cooccurTermParams2[0]+"\t"+str(cooccurCount)+"\t"+str(statCooccur)+ "\t"+":-:".join(cooccurOntos)+"\n")

