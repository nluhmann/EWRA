#!/usr/bin/env python
import sys
import re

######
#extract all adjacencies from the extant marker and the assembly graph
######




hitfile = sys.argv[1]
dotfile = sys.argv[2]
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


########################################################################################
print "read dot file"
def readDotFile(dotfile):
	connected = {}
	file = open(dotfile, "r")
	for line in file:
		if "->" in line: 
			array = line.split('"')
			start = array[1]
			stop = array[3]
			#contigIDs bleiben mit + und - damit kein Durcheinander!
			if start in connected:
				connected[start].append(stop)
			else:
				liste = []
				liste.append(stop)
				connected[start] = liste
			
	file.close()
	return connected




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
			
			#extract infos for assembly rgaph
			contigID = parts[1].split(' ')[2]
			contigStart = parts[2].split('-')[0]
			tupel = (int(contigStart), (markerTail, markerHead))
			if contigID in assemblyhash:
				if tupel not in assemblyhash[contigID]:
					assemblyhash[contigID].append(tupel)
			else:
				liste = []
				liste.append(tupel)
				assemblyhash[contigID] = liste
				
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
def findAdjacencies(specieslist, hash, assemblyhash, connected):
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

	
	
	for contig in assemblyhash:
		liste = assemblyhash[contig]
		#only one marker on the contig, only need to check graph connections:
		if len(liste) == 1:
			#check connected contigs in the graph in both directions
			pluscontig = contig+"+"
			minuscontig = contig+"-"
			leftExtrem = liste[0][1][0]
			rightExtrem = liste[0][1][1]
			adjacencies = checkAssemblyGraphConnections(pluscontig, minuscontig, leftExtrem, rightExtrem, connected, adjacencies)
						
										

		#more than one marker on the contig, check adjacencies in the contig itself first, then graph connections for bordering extremities	
		else:
		
			#save adjacencies on the contig itself		
			
			for i in range(len(liste)-1):
				
				#take right extremity of left marker and left extremity of right marker and reverse
				tupel = (liste[i][1][1], liste[i+1][1][0])
				revtupel = (liste[i+1][1][0], liste[i][1][1])
				adjacencies = setAdjacencies(tupel, revtupel, adjacencies)
				intraCon.append(tupel)
				intraCon.append(revtupel)
					
			#then save adjacencies from bordering marker to connected contigs in the graph in both directions
			pluscontig = contig+"+"
			minuscontig = contig+"-"
			leftExtrem = liste[0][1][0]
			rightExtrem = liste[-1][1][1]
			adjacencies = checkAssemblyGraphConnections(pluscontig, minuscontig, leftExtrem, rightExtrem, connected, adjacencies)
			
			
		
			
	return adjacencies



###########################################################################################################################################################
def setAdjacencies(tupel, revtupel, adjacencies):
	global counterOnly
	global counterTupel
	global counterRev
	if testTupel(tupel):
		if tupel in adjacencies:
			counterTupel = counterTupel + 1
			adjacencies[tupel][len(adjacencies[tupel])-1] = 1
		elif revtupel in adjacencies:
			counterRev = counterRev + 1
			adjacencies[revtupel][len(adjacencies[revtupel])-1] = 1
		else:
			counterOnly = counterOnly + 1
			adjacencies[tupel] = [0 for i in range(len(specieslist)+1)]
			adjacencies[tupel][len(adjacencies[tupel])-1] = 1
	

	return adjacencies
	






###########################################################################################################################################################
def checkAssemblyGraphConnections(pluscontig, minuscontig, leftExtrem, rightExtrem, connected, adjacencies):
	minusConnected = []
	plusConnected = []
	if minuscontig in connected:
		minusConnected = connected[minuscontig]
	if pluscontig in connected:
		plusConnected = connected[pluscontig]
		
	
	#wenn A+ mit B+ (= B- mit A-) verbunden ist, besteht ein ueberlapp zwischen dem Suffix von A und dem Praefix von B.
	#d.h., speichere adjacency zwischen dem letzten marker auf A und dem ersten auf B
	#wenn A+ mit B- (=B+ mit A-) verbunden ist, besteht ein ueberlapp zwischen dem Suffix von A und dem Praefix von B reverse komplement.
	#d.h., speichere adjacency zwischen dem letzten marker auf A und dem letzten auf B
	#wenn A- mit B+ (=B- mit A+) verbunden ist, besteht ein ueberlapp zwischen dem Suffix von A reverse komplement und dem Praefix von B.
	#d.h., speichere adjacency zwischen dem ersten marker auf A und dem ersten auf B
	#wenn A- mit B- (=B+ mit A+) verbunden ist, besteht ein ueberlapp zwischen dem Suffix von A reverse komplement und dem Praefix von B reverse komplement.
	#d.h., speichere adjacency zwischen dem ersten marker auf A und dem letzten auf B
	
	
	#connected to minus	
	if len(minusConnected) >= 1:
		for minus in minusConnected:
			if minus[:-1] in assemblyhash:
				liste = assemblyhash[minus[:-1]]
				#if minus is +, take last extremity on this contig (because of its direction), if minus is -, take first extremity on this contig
				if minus[-1] == "-":
					lastExtrem = liste[-1][1][1]
					tupel = (leftExtrem, lastExtrem)
					revtupel = (lastExtrem, leftExtrem)
					adjacencies = setAdjacencies(tupel, revtupel, adjacencies)
					#ACHTUNG, so koennen doppelte gespeichert werden!
					interCon.append(tupel)
					interCon.append(revtupel)
				elif minus[-1] == "+":
					if not rightExtrem in liste[0][1] and not leftExtrem in liste[0][1]:
						firstExtrem = liste[0][1][0]
						tupel = (leftExtrem, firstExtrem)
						#print tupel
						revtupel = (firstExtrem, leftExtrem)
						adjacencies = setAdjacencies(tupel, revtupel, adjacencies)
						interCon.append(tupel)
						interCon.append(revtupel)
				else:
					print "error"	
					
									
				
	#connected to plus
	if len(plusConnected) >= 1:
		for plus in plusConnected:
			if plus[:-1] in assemblyhash:
				liste = assemblyhash[plus[:-1]]
				#if plus is +, take last extremity on this contig (because of its direction), if plus is -, take first extremity on this contig
				if plus[-1] == "-":
					
					#print tupel
					#here is also something wrong!
					if not rightExtrem in liste[-1][1] and not leftExtrem in liste[-1][1]:
						lastExtrem = liste[-1][1][1]
						tupel = (rightExtrem, lastExtrem)
						revtupel = (lastExtrem, rightExtrem)
						adjacencies = setAdjacencies(tupel, revtupel, adjacencies)
						interCon.append(tupel)
						interCon.append(revtupel)
				elif plus[-1] == "+":
					firstExtrem = liste[0][1][0]
					tupel = (rightExtrem, firstExtrem)
					revtupel = (firstExtrem, rightExtrem)
					adjacencies = setAdjacencies(tupel, revtupel, adjacencies)
					interCon.append(tupel)
					interCon.append(revtupel)
				else:
					print "error"
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
def numberOfConflictingAdjacencies(adjacencies):
	conflicts = 0
	hash = {}
	for adjacency in adjacencies:
		left = adjacency[0]
		right = adjacency[1]
		if left in hash:
			conflicts = conflicts + 1
			print left
		else:
			hash[left] = 1
		
		if right in hash:
			conflicts = conflicts + 1
			print right
		else:
			hash[right] = 1


	

###########################################################################################################################################################
specieslist = readSpeciesTree(treefile)
connected = readDotFile(dotfile)
readFamilies(hitfile, specieslist)
sortedHash = sortTupels(hash)
sortedAssemblyHash = sortTupels(assemblyhash)
adj = findAdjacencies(specieslist, sortedHash, sortedAssemblyHash, connected)
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
	