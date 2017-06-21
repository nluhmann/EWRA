#!/usr/bin/env python
import sys
import re

######
#extract all adjacencies from the extant marker and the assembly graph
######
# python $SRC/extractAdjacencies.py $FILTERED_FAMILIES $PRUNED_GRAPH $TREE $ALL_ADJACENCIES




hitfile = sys.argv[1]
filled_gaps_coordinates = sys.argv[2]
treefile = sys.argv[3]
outputfile = sys.argv[4]

counterTupel = 0
counterRev = 0
counterOnly = 0
intraCon = []
interCon = []

##########################################################################################
#read the tree and return a list of all species in the tree
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





####################################################################################################################################################################################
# key: species name, value: list of tupel (startpos, (marker extremities according to orientation))	
hash = {}
# key: contigID, value: list of tupel (startpos, marker extremities)	
assemblyhash = {}

### Reading families file, check with contig names			
def readFamilies(filename, specieslist):
	
	# initialize hash based on species list
	for species in specieslist:
		list = []
		hash[species] = list
	
		
	checkspecieslist = [0 for i in range(len(specieslist))]
	savelist = []
	id =""
	countRemoved = 0
	countSaved = 0
	datei = open(filename, "r")

	
	for line in datei:
		if line.startswith('>'):
			markerID = line[1:].replace("\n","")
			markerHead = int(markerID)*2
			markerTail = (int(markerID)*2)-1
		elif len(line) > 1:
			parts = line.rstrip("\n").split(':')
			#extract infos for extant genome
			orientation = parts[1].split(" ")[1]
			extantName = parts[0].split('.')[0]
			extantStart = parts[1].split('-')[0]
			if orientation is "+":
				extremities = (markerTail, markerHead)
			elif orientation is "-":
				extremities = (markerHead, markerTail)
			else:
				print "Orientation error"
			tupel = (int(extantStart), extremities)
			hash[extantName].append(tupel)
				
	datei.close()			
	
#########################################################################################
### Tupelsorting
def sortTupels(hash):
	for key in hash:
		hash[key].sort()
	return hash		
	

##########################################################################################
### Tupeltesting
def testTupel(tupel):
	first = tupel[0]
	second = tupel[1]
	bool = True
	if first > second:
		if first % 2 == 0:
			if first - second == 1:
				bool = False
	elif second > first:
		if second % 2 == 0:
			if second - first == 1:
				bool = False
	
	return bool


###########################################################################################
### Adjacencies are contiguous entries in sorted hash for each species	
def findAdjacencies(specieslist, hash, filled_gaps):
	# key: adjacency as tupel of two marker, value: array the length of the specieslist +1 for the ancient assembly
	adjacencies = {}
	
	#save adjacencies for extant genomes
	for species in specieslist:
			list = hash[species]
			for i in range(len(list)-1):
				tupel = (list[i][1][1], list[i+1][1][0])
				revtupel = (list[i+1][1][0], list[i][1][1])
				
				if testTupel(tupel):
					if tupel in adjacencies:
						adjacencies[tupel][specieslist.index(species)] = 1
					elif revtupel in adjacencies:
						adjacencies[revtupel][specieslist.index(species)] = 1
					else:
						adjacencies[tupel] = [0 for i in range(len(specieslist)+1)]
						adjacencies[tupel][specieslist.index(species)] = 1

	
	
	file = open(filled_gaps,"r")
	for line in file:
		fields = line.split(" ")
		leftMarker = int(fields[2].split("-")[0])
		rightMarker = int(fields[2].split("-")[1])
		
		tupel = (leftMarker, rightMarker)
		revtupel = (rightMarker, leftMarker)
		
		if tupel in adjacencies:
			adjacencies[tupel][-1] = 1
		elif revtupel in adjacencies:
			adjacencies[revtupel][-1] = 1
		else:
			adjacencies[tupel] = [0 for i in range(len(specieslist)+1)]
			adjacencies[tupel][-1] = 1
		
			
			
		
			
	return adjacencies

	


	
	
###########################################################################################################################################################
# write adjacency output
def writeAdjacencies(specieslist, adjacencies):
	file = open(outputfile, "w")
	for item in specieslist:
  		file.write("%s," %item)
  	file.write("AssemblyGraphLeaf")
  	file.write("\n")
	
	
	for adjacency in adjacencies:
		file.write(">("+str(adjacency[0])+","+str(adjacency[1])+")"+" [")
		for item in adjacencies[adjacency]:
			file.write(str(item)+",")
		file.write("]\n")
		
	file.close()	


	

###########################################################################################################################################################
specieslist = readSpeciesTree(treefile)
readFamilies(hitfile, specieslist)
sortedHash = sortTupels(hash)
adj = findAdjacencies(specieslist, sortedHash, filled_gaps_coordinates)
writeAdjacencies(specieslist, adj)
###########################################################################################################################################################




##########
#output files for statistics
##########
file = open("./intraCon.txt", "w")
for con in intraCon:
	first = con[0]
	second = con[1]
	file.write(str(first)+ " -> "+str(second)+"\n")
file.close()
file = open("./interCon.txt", "w")
for con in interCon:
	first = con[0]
	second = con[1]
	file.write(str(first)+ " -> "+str(second)+"\n")
file.close()
	