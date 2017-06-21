#!/usr/bin/env python

#####
#remove all families that are not uniquely present in all extant genomes.
#####

import re
import sys
input = sys.argv[1]
output = sys.argv[2]
treefile = sys.argv[3]



def readSpeciesTree(treefile):
	species = []
	file = open(treefile, "r")
	for line in file:
		list = line.split(",")
		for elem in list:
			name = re.search('\(*([0-9A-Za-z\_]*)', elem).group(1)
			species.append(name)
	file.close()		
	return species


specieslist = readSpeciesTree(treefile)
checkspecieslist = [0 for i in range(len(specieslist))]


datei = open(input, "r")
counter = 0
markerID = ""
savedLines = ""
file = open(output, "w")
for line in datei:
		if line.startswith('>'):
			if checkspecieslist.count(1) == len(checkspecieslist) and markerID != "" and counter == len(specieslist):
				
				file.write(markerID)
				file.write(savedLines)
				
			markerID = line
			counter = 0
			checkspecieslist = [0 for i in range(len(specieslist))]
			savedLines = ""
		elif len(line) > 1:
			parts = line.split(':')
			name = parts[0].split('.')[0]
			checkspecieslist[specieslist.index(name)] = 1
			counter = counter + 1
			savedLines = savedLines + line
		

if checkspecieslist.count(1) == len(checkspecieslist) and markerID != "" and counter == len(specieslist):
				
				file.write(markerID)
				file.write(savedLines)			
file.close()




