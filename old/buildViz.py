import sys
import json


nodesFile = open(sys.argv[1])
nodes = nodesFile.readlines()
nodesFile.close()

edgesFile = open(sys.argv[2])
edges = edgesFile.readlines()
edgesFile.close()

ontoCoccurFile = open(sys.argv[3])
ontoTermLines = ontoCoccurFile.readlines()
ontoCoccurFile.close()
ontoTermLocator = {}

outputJson = open(sys.argv[4], "w+")

for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    ontoTermLocator[ontoTermParams[0]] = ontoTermParams[1]

nodesLocator = {}
formatedNodes = []
formatedEdges = []

for i in range(len(nodes)):
    nodeParams = nodes[i].strip().split("\t")
    formatedNodes.append({"name": ontoTermLocator.get(nodeParams[0]), "uri": nodeParams[0], "group": int(nodeParams[1])})
    nodesLocator[nodeParams[0]] = i

for i in range(len(edges)):
    nodeParams = edges[i].strip().split("-->")
    formatedEdges.append({"source": nodesLocator[nodeParams[0]], "target": nodesLocator[nodeParams[1]], "value": 1})

outputJson.write(json.dumps({"nodes": formatedNodes, "links": formatedEdges}))
