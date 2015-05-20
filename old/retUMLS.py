import os
import sys
import urllib2
import json

REST_URL = "http://data.bioontology.org"
API_KEY = "5b7f7e20-015c-496f-ade9-ca341345cef7"

output = open("UMLSontologies.tsv" , "w+")

def get_json(url):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
        return json.loads(opener.open(url).read())
    except urllib2.HTTPError:
        print 'Error Encountered'
        return None

for root, dirs, files in os.walk(u"ontologies/"):
    for file in files:
        url = REST_URL+"/ontologies/" + file.strip().split('--')[0] + "/groups"
        print url
        groups = get_json(url)
        if groups: 
            if groups[0]["acronym"] == "UMLS":
               print file.strip().split('--')[0]
               output.write(file.strip().split('--')[0] + "\n")
        