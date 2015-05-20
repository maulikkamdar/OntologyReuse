import os
import sys
import json

#OntoSourceCooccurFile
ontoCoccurFile = open(sys.argv[1])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()

termCountFile = open(sys.argv[2])
termCounts = termCountFile.readlines()
termCountFile.close()

outputJson = open(sys.argv[3], "w+")
reuseStatsFile = open("reuseStatsFileaViews.tsv", "w+")
isReusedStatsFile = open("isReusedStatsFileaViews.tsv", "w+")

ontologyCategoriesFile = open(sys.argv[4])
ontologyCategoriesLines = ontologyCategoriesFile.readlines()
ontologyCategoriesFile.close()

naTerms = []
naTermFile = open(sys.argv[5])
naTermLines = naTermFile.readlines()
naTermFile.close()

for i in naTermLines:
    naTerms.append(i.strip())

ontologyCategories = {}
for i in ontologyCategoriesLines:
    ontologyParams = i.strip().split("\t")
    ontologyCategories[ontologyParams[0]] = {"name": ontologyParams[1], "description": ontologyParams[2] + "<br>" + ontologyParams[3], "cluster": int(ontologyParams[4])}

termCountsLoc = {}
reuseStats = {}
isReusedStats = {}
nodes = []
nodeLocator = {}
edges = []
edgeLocator = {}

edgesFile = open("edgesAllaViews.tsv", "w+")

def getNode(identifier):
    if not nodeLocator.get(identifier):
        if termCountsLoc.get(identifier):
            size = termCountsLoc[identifier]
        else:
            size = 1
        if identifier in ontologyCategories:
            name = ontologyCategories[identifier]["name"]
            description = ontologyCategories[identifier]["description"]
            cluster = ontologyCategories[identifier]["cluster"]
        else:
            name = identifier
            description = identifier
            cluster = 0
        nodes.append({"name": name, "description": description, "cluster": cluster, "size": size, "number": len(nodes), "identifier": identifier})
        nodeLocator[identifier] = len(nodes)-1
    else:
        if not termCountsLoc.get(identifier):
            nodes[nodeLocator[identifier]]["size"] = nodes[nodeLocator[identifier]]["size"] + 1
    return nodeLocator[identifier]


for i in range(len(termCounts)):
    termCountParams = termCounts[i].strip().split("\t")
    termCountsLoc[termCountParams[0]] = int(termCountParams[1])

for i in range(len(ontoTermLines)):
    #print ontoTermLines[i]
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    if ontoTermParams[0].strip() in naTerms:
        continue

    ontologies = ontoTermParams[3].strip().split(":-:")
    sourceOntology = ontoTermParams[4].strip()

    if termCountsLoc.get(sourceOntology):
        print sourceOntology
        if isReusedStats.get(sourceOntology):
            isReusedStats[sourceOntology] = isReusedStats[sourceOntology] + 1
        else:
            print "here"
            isReusedStats[sourceOntology] = 1
    sourceId = getNode(sourceOntology)

    for k in ontologies:
        if k != sourceOntology:
            if termCountsLoc.get(k):
                if reuseStats.get(k):
                    reuseStats[k] = reuseStats[k] + 1
                else:
                    reuseStats[k] = 1
            targetId = getNode(k)
            if edgeLocator.get(sourceOntology + ":-:" + k):
                edges[edgeLocator[sourceOntology + ":-:" + k]]["value"] = edges[edgeLocator[sourceOntology + ":-:" + k]]["value"] + 1
            else:
                edges.append({"source": sourceId, "target": targetId, "value": 1, "id": len(edges)})
                edgeLocator[sourceOntology + ":-:" + k] = len(edges)-1
            
               
for i in reuseStats:
    reuseStatsFile.write(i + "\t" + str(reuseStats[i]) + "\t" + str(termCountsLoc[i]) + "\n")

for i in isReusedStats:
    isReusedStatsFile.write(i + "\t" + str(isReusedStats[i]) + "\t" + str(termCountsLoc[i]) + "\n")

outputJson.write(json.dumps({"nodes": nodes, "edges": edges}))

for i in edges:
    edgesFile.write(nodes[i["target"]]["identifier"] + "\t" + nodes[i["source"]]["identifier"] + "\t" +  str(i["value"]) + "\n")