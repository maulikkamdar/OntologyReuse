import os
import sys
import re
import networkx as nx

nodeCount = 0
G = nx.Graph()
fileCount =  0

def checkNode(identifier, strLabel):
	global nodeCount
	if not G.has_node(identifier):
		G.add_node(identifier, label=strLabel)
		nodeCount = nodeCount + 1
	return identifier

def main():
	#combCompositeTerms (Same IRI merged)
	global nodeCount
	global fileCount
	global G
	nodeIris = {}
	ontologyList = {}
	compositeFile = open(sys.argv[1])
	compositeMappings = compositeFile.readlines()
	compositeFile.close()

	#mappedFile using Heuristics
	heurFile = open(sys.argv[2])
	heurMappings = heurFile.readlines()
	heurFile.close()
	for k in range(len(compositeMappings)):
		if k == 0: 
			continue
		compositeParams = compositeMappings[k].strip().split("\t")
		nodeIris[compositeParams[0]] = k
		print k
		ontologies = compositeParams[1].strip().split(":-:")
		for onto in ontologies:
			if not ontologyList.get(onto):
				ontologyList[onto] = len(ontologyList) + 1
				#nodeCount = nodeCount + 1
				#G.add_node("Ont" + str(ontologyList[onto]), label = onto)


	for k in range(len(heurMappings)):
		if k == 0:
			continue
		heurParams = heurMappings[k].strip().split("\t")

		print heurParams[0] + "\t :-:" + str(k)
		iris = heurParams[1].split(":-::-:")
		ontologyGroups = heurParams[2].split(":-::-:")
		types = heurParams[3].split(":-::-:")
		
		for m in range(len(iris)):
			nodeId1 = checkNode(nodeIris[iris[m]], iris[m])
			ontologies = ontologyGroups[m].split(":-:")
			for onto in ontologies:
				ontoId = checkNode("Ont" + str(ontologyList[onto]), onto)
				G.add_edge(nodeId1, ontoId, type = "O")

			for n in range(m+1, len(iris)):
				nodeId2 = checkNode(nodeIris[iris[n]], iris[n])
				if types[m] > types[n]:
					typeStr = types[n] + types[m]
				else:
					typeStr = types[m] + types[n]

				if not G.has_edge(nodeId1, nodeId2):
					G.add_edge(nodeId1, nodeId2, type=typeStr, content=heurParams[0])
				elif G[nodeId1][nodeId2]['type'] > typeStr: # we found a stricter match!
					G[nodeId1][nodeId2]['type'] = typeStr
					G[nodeId1][nodeId2]['content'] = heurParams[0]


		if nodeCount > int(sys.argv[4]):
			fileCount = fileCount + 1
			nx.write_gpickle(G, sys.argv[3] + "_" + str(fileCount) + ".gpickle")
			G = nx.Graph()
			nodeCount = 0

main()

