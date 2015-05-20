import urllib2
import json

REST_URL = "http://data.bioontology.org"
API_KEY = "5b7f7e20-015c-496f-ade9-ca341345cef7"

def get_json(url):
    print url
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
        return json.loads(opener.open(url).read())
    except urllib2.HTTPError:
        print 'Error Encountered'
        return None

# Get all ontologies from the REST service and parse the JSON
ontologies = get_json(REST_URL+"/ontologies")
output = open("ontologyNamesGroups1.tsv", 'w+')
count = 0

defgroups = {}
defgroups["OBO_Foundry"] = 1
defgroups["UMLS"] = 2

clusterCount = 2

if ontologies:
    for ontology in ontologies:
        count = count + 1
        print str(count) + "\t" + ontology["acronym"]
        groups = get_json(REST_URL + "/ontologies/" + ontology["acronym"] + "/groups")
        categories = get_json(REST_URL + "/ontologies/" + ontology["acronym"] + "/categories")

        cluster = 0
        ontoGroups = "Groups: "
        ontoCategories = "Categories: "
        hasGroups = []
        if groups:
            for k in range(len(groups)):
                if k == 0:
                    ontoGroups = ontoGroups + groups[k]["acronym"]
                else:
                    ontoGroups = ontoGroups + ", " + groups[k]["acronym"]
                hasGroups.append(groups[k]["acronym"])
                if not groups[k]["acronym"] in defgroups:
                    clusterCount = clusterCount + 1
                    defgroups[groups[k]["acronym"]] = clusterCount 
            if "OBO_Foundry" in hasGroups:
                cluster = defgroups["OBO_Foundry"]
            elif "UMLS" in hasGroups:
                cluster = defgroups["UMLS"]
            else:
                cluster = defgroups[hasGroups[0]]
        

        if categories:
            for k in range(len(categories)):
                if k == 0:
                    ontoCategories = ontoCategories + categories[k]["acronym"]
                else:
                    ontoCategories = ontoCategories + ", " + categories[k]["acronym"]

        output.write(ontology["acronym"] + "\t" + ontology["name"] + "\t" + ontoGroups + "\t" + ontoCategories + "\t" + str(cluster) + "\n")
