# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import re

imported = open("importedOntologies.tsv")
imports = [x.strip() for x in imported.readlines()]
imported.close()

hasOnto = []
for root, dirs, files in os.walk(u"../stage_rdf_dump/ontologies/"):
    for file in files:
        ontoid = file.strip().split('--')[0]
        hasOnto.append(ontoid)

for k in imports:
    if not k in hasOnto:
        print k