#!/usr/bin/python

import os
import shutil

ontologies = {}
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(u"."):
    for file in files:
        #print len(path)*'---', file
        ontoVersionFile = open(root + '/' + file)
        ontoInfo = ontoVersionFile.readline()
        ontoParts = ontoInfo.strip().split('/')
        if len(ontoParts) > 6 and ontoParts[3] == "ontologies":
            if ontologies.get(ontoParts[4]):
                if ontologies[ontoParts[4]][0] < ontoParts[6]:
                    ontologies[ontoParts[4]] = (ontoParts[6], root+'/'+file)
            else:
                ontologies[ontoParts[4]] = (ontoParts[6], root+'/'+file)

for ontology in ontologies:
    print ontology + ':-:' + ontologies[ontology][0] + ':-:' + ontologies[ontology][1]
    shutil.copyfile(ontologies[ontology][1], './ontologies/'+ontology+'--'+ontologies[ontology][0])

