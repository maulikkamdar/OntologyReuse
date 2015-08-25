import os
import sys
import re


#combCompositeTerms (Same IRI merged)
compositeFile = open(sys.argv[1])
compositeMappings = compositeFile.readlines()
compositeFile.close()

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

uniqueStrings = {}

mergedCompoFile = open(sys.argv[2], "w+")

for k in range(len(compositeMappings)):
	if k == 0:
		mergedCompoFile.write("String\tIRIs\tOntologies\tTypes\n")
		continue
	compositeParams = compositeMappings[k].strip().split("\t")
	if len(compositeParams) > 2:
		for syn in range(2, len(compositeParams)):
			if syn == 2:
				synonym_type = "A" 
			elif syn == 3:
				synonym_type = "E"
			elif syn == 4:
				synonym_type = "R"
			else:
				synonym_type = "U"
			for word in compositeParams[syn].strip().split(":-:"):
				if len(word) > 0:
					normalizedVector = normalize(word)
	            	# do something for the other synonyms
					normalizedWord = " ".join(sorted(normalizedVector)).lower().strip()
					print normalizedWord
					if len(normalizedWord) > 0:
						if uniqueStrings.get(normalizedWord):
							if not compositeParams[0] in uniqueStrings[normalizedWord]["iri"]:
								uniqueStrings[normalizedWord]["iri"].append(compositeParams[0])
								uniqueStrings[normalizedWord]["type"].append(synonym_type)
								uniqueStrings[normalizedWord]["ontologies"].append(compositeParams[1])
								uniqueStrings[normalizedWord]["count"] = uniqueStrings[normalizedWord]["count"] + len(compositeParams[1].strip().split(":-:"))
							else:
								if synonym_type < uniqueStrings[normalizedWord]["type"][uniqueStrings[normalizedWord]["iri"].index(compositeParams[0])]:
									uniqueStrings[normalizedWord]["type"][uniqueStrings[normalizedWord]["iri"].index(compositeParams[0])] = synonym_type
						else:
							uniqueStrings[normalizedWord] = {"iri": [compositeParams[0]], "type": [synonym_type], "ontologies": [compositeParams[1]], "count": len(compositeParams[1].strip().split(":-:"))}


print len(uniqueStrings)
totalCount = 0
for mapping in uniqueStrings:
	if len(uniqueStrings[mapping]["iri"]) == 1 and len(uniqueStrings[mapping]["ontologies"][0].split(":-:")) == 1:
		continue
	mergedCompoFile.write(mapping + "\t" + ":-::-:".join(uniqueStrings[mapping]["iri"]) + "\t" + ":-::-:".join(uniqueStrings[mapping]["ontologies"]) + "\t" + ":-::-:".join(uniqueStrings[mapping]["type"]) + "\n")
	totalCount = totalCount + uniqueStrings[mapping]["count"]

print totalCount


