import urllib2
import json

REST_URL = "http://data.bioontology.org"
API_KEY = "5b7f7e20-015c-496f-ade9-ca341345cef7 "

def get_json(url):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
        return json.loads(opener.open(url).read())
    except urllib2.HTTPError:
        print 'Error Encountered'
        return None

# Get all ontologies from the REST service and parse the JSON
ontologies = get_json(REST_URL+"/ontologies")
output = open("ontologyRest.tsv", 'w+')
count = 0

if ontologies:
    for ontology in ontologies:
        count = count + 1
        print ontology["acronym"]
        views = get_json(REST_URL + "/ontologies/" + ontology["acronym"] + "/views")
        viewList = ""
        if views:
            for view in views:
                count = count + 1
                viewList = view["acronym"] + ":-:"
        output.write(ontology["acronym"] + "\t"+ viewList + "\n")

print count
