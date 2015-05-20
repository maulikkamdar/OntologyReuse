import sys
import json
import re

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
ontoColorScale = open(sys.argv[5])
ontoColors = ontoColorScale.readlines()

formatedNodes = {}
formatedEdges = []

'''for i in range(len(ontoTermLines)):
    ontoTermParams = ontoTermLines[i].strip().split("\t")
    ontoSplitTerms = re.split(r'[/#]',ontoTermParams[0])
    identifier = ontoSplitTerms[len(ontoSplitTerms)-1]
    ontoTermLocator[ontoTermParams[0]] = identifier + ":-:" + ontoTermParams[1]

nodesLocator = {}
'''

for i in range(len(nodes)):
    nodeParams = nodes[i].strip().split("\t")
    node0Terms = re.split(r'[/#]',nodeParams[0])
    if int(nodeParams[1]) != 100:
        formatedNodes[node0Terms[len(node0Terms)-1]] = "#" + ontoColors[int(nodeParams[1])].strip()
    else:
        formatedNodes[node0Terms[len(node0Terms)-1]] = "#" + ontoColors[40].strip()

for i in range(len(edges)):
    nodeParams = edges[i].strip().split("-->")
    node1Terms = re.split(r'[/#]',nodeParams[1])
    node0Terms = re.split(r'[/#]',nodeParams[0])
    fromTxt = node1Terms[len(node1Terms)-1]
    toTxt = node0Terms[len(node0Terms)-1]
    formatedEdges.append({"from": fromTxt, "to": toTxt})

outputJson.write(json.dumps(formatedNodes))
outputJson.write("\n-----\n")
outputJson.write(json.dumps(formatedEdges))
