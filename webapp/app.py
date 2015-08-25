from flask import Flask, render_template, json, request
import networkx as nx
import re

app = Flask(__name__)
nodeList = {}
termStrList = {}
reducedGraph = "data/reducedGraph.gpickle"
allTerms = "data/combCompositeTerms.tsv"
heuristicMappings = "data/heurCompositeTerms.tsv"
pageLength = 25

SG = nx.read_gpickle(reducedGraph)
print "Read Graph"

compositeFile = open(allTerms)
compositeMappings = compositeFile.readlines()
compositeFile.close()
#mappedFile using Heuristics

heurFile = open(heuristicMappings)
heurMappings = heurFile.readlines()
heurFile.close()

for k in range(len(compositeMappings)):
	if k == 0: 
		continue
	#print k
	compositeParams = compositeMappings[k].strip().split("\t")
	nodeList[compositeParams[0]] = k

print "Completed reading composite information"

for k in range(len(heurMappings)):
	if k == 0:
		continue
	heurParams = heurMappings[k].strip().split("\t")
	termStrList[heurParams[0]] = heurParams[1]

print "Read all classes information and heuristic mappings"

#--- string retrieval funcitons 

stopWords = set([
    "a", "also", "although", "am", "an", "and", "are",
    "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "being", "bill", "both",
    "bottom", "but", "by", "call", "can", "con",
    "could", "de", "do", "done", "eg", "etc", "even", "ever", 
    "find", "for", "found", "from", "get", "give", "go",
    "had", "has", "have", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "however", "if", "in", "inc", 
    "into", "is", "it", "its", "itself", "keep", "may", "me", "mine", "my", "myself", "name", "namely", "of", "onto", "our",
    "ours", "ourselves", "please", "put", "should", "show", "such", "take", "that", "the", "their", "them",
    "themselves", "these", "they", "this", "those", "though",
    "thru", "to", "us", "via", "was", "we", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "whither",
    "who", "whoever", "whom", "whose", "why", "will", "would", "yet", "you", "your", "yours", "yourself", "yourselves"])

def normalize(word):
    word = word.replace('\n', ' ').lower()
    word = re.sub('[^0-9a-zA-Z]+', " ", word)
    vec1 = re.split("\\s+", word)
    vec1 = [x for x in vec1 if x not in stopWords]
    return vec1

def almostAssocTerms(word):
	return [] #modify this

@app.route("/")
def main():
	return render_template('index.html')

@app.route('/similarTerms', methods=['POST'])
def similarTerms():
	_termStr = request.form['termString']
#def similarTerms(termString):
#	_termStr = termString
	normalizedVector = normalize(_termStr)
	normalizedWord = " ".join(sorted(normalizedVector)).lower().strip()
	currentList = {}

	if normalizedWord in termStrList:
		iris = termStrList[normalizedWord].strip().split(":-::-:")
	else:
		iris = almostAssocTerms(normalizedWord)

	firstDegree = []
	
	for k in range(len(iris)):
		currentList[nodeList[iris[k]]] = {"degree": 0, "type": "Ex", "compositeMappings": compositeMappings[nodeList[iris[k]]], "outward": []} 
		for node in SG[nodeList[iris[k]]]:
			nodeInfo = SG[nodeList[iris[k]]][node]
			if node not in currentList:
				currentList[node] = {"type": nodeInfo["type"], "content": nodeInfo["content"], "degree": 1, "outward": [nodeList[iris[k]]], "compositeMappings": compositeMappings[node]}
				firstDegree.append(node)
			else: 
				if nodeInfo["type"] < currentList[node]["type"] and currentList[node]["degree"] > 0:
					currentList[node]["type"] = nodeInfo["type"]
					currentList[node]["content"] = nodeInfo["content"]
				currentList[node]["outward"].append(nodeList[iris[k]])

	for k in range(len(firstDegree)):
		for node in SG[firstDegree[k]]:
			nodeInfo = SG[firstDegree[k]][node]
			if node not in currentList:
				currentList[node] = {"type": nodeInfo["type"], "content": nodeInfo["content"], "degree": 2, "outward": [firstDegree[k]], "compositeMappings": compositeMappings[node]}
			else: 
				if nodeInfo["type"] < currentList[node]["type"] and currentList[node]["degree"] > 0:
					currentList[node]["type"] = nodeInfo["type"]
					currentList[node]["content"] = nodeInfo["content"]
				currentList[node]["outward"].append(firstDegree[k])
	
	output = {"0Ex": [], "1AA": [], "1AE": [], "1AR": [], "1AU" : [], "1EE": [], "1ER" : [], "1EU" : [], "1RR":[], "1RU" : [], "1UU": [], "2AA" : [], "2AE": [], "2AR": [], "2AU": [], "2EE": [], "2ER": [], "2EU": [], "2RR": [], "2RU": [], "2UU": []}

	for node in currentList:
		identifer = str(currentList[node]["degree"]) + currentList[node]["type"]
		output[identifer].append({"index" : node, "compositeParams": currentList[node]["compositeMappings"].strip().split("\t"), "outward": [] if identifer = "0Ex" else currentList[node]["outward"]})
	return json.dumps(output)


if __name__ == "__main__":
	app.run()



