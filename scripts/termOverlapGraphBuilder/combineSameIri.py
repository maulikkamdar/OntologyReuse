import os
import sys

compositeFile = open(sys.argv[1])
compositeMappings = compositeFile.readlines()
compositeFile.close()

mergedCompoFile = open(sys.argv[2], "w+")
terms = {}

for k in range(len(compositeMappings)):
	if k == 0:
		mergedCompoFile.write("Term URI\tOntology\tLabels\tExact\tRelated\tOther\n")
		continue
	compoParams = compositeMappings[k].strip().split("\t")
	print compoParams[0]
	if terms.get(compoParams[0]):
		terms[compoParams[0]]["ontologies"].append(compoParams[1])
		if not compoParams[2] in terms[compoParams[0]]["label"]:
			terms[compoParams[0]]["label"].append(compoParams[2])
		if len(compoParams) > 6:
			terms[compoParams[0]]["exact"] = list(set(terms[compoParams[0]]["exact"]) | set(compoParams[6].strip().split(":-:")))
		if len(compoParams) > 7:
			terms[compoParams[0]]["related"] = list(set(terms[compoParams[0]]["related"]) | set(compoParams[7].strip().split(":-:")))
		if len(compoParams) > 8:
			terms[compoParams[0]]["other"] = list(set(terms[compoParams[0]]["other"]) | set(compoParams[8].strip().split(":-:")))
	else:
		terms[compoParams[0]] = {"iri": compoParams[0], "label": [compoParams[2]], "ontologies" : [compoParams[1]], "exact": [], "related": [], "other": []}
		if len(compoParams) > 6:
			terms[compoParams[0]]["exact"].extend(compoParams[6].strip().split(":-:"))
		if len(compoParams) > 7:
			terms[compoParams[0]]["related"].extend(compoParams[7].strip().split(":-:"))
		if len(compoParams) > 8:
			terms[compoParams[0]]["other"].extend(compoParams[8].strip().split(":-:"))



for term in terms:
	mergedCompoFile.write(term + "\t" + ":-:".join(terms[term]["ontologies"]) + "\t" + ":-:".join(terms[term]["label"]) + "\t" + ":-:".join(terms[term]["exact"]) + "\t" + ":-:".join(terms[term]["related"]) + "\t" + ":-:".join(terms[term]["other"]) + "\n")


