import sys


hartiganfile = sys.argv[1]

fitchfile = sys.argv[2]

#ancestral = sys.argv[3]


# double marker id to account for orientation
def doubleMarker(marker):
    if "-" in marker:
        return int(marker[1:]) * 2, (int(marker[1:]) * 2) - 1
    else:
        return (int(marker) * 2) - 1, int(marker) * 2




# double marker and find adjacencies in chromosomes
def findAdjacencies(speciesHash):
    #print "collect extant adjacencies from marker file..."
    # keys: (left marker, right marker), value: [(species,chromosome),...]
    # keys: (species), value: (left marker right marker)
    adjacencies = {}
    for species in speciesHash:
        chromosomes = speciesHash[species]
        adjacencies[species] = []
        for chrom in chromosomes:
            orderList = chromosomes[chrom]
            for i in range(0,len(orderList)-1):
                first = orderList[i]
                second = orderList[i+1]
                doubleFirst = doubleMarker(first)
                doubleSecond = doubleMarker(second)
                #take right extrem of first and left extrem of second for adj tuple
                if (int(doubleFirst[1]) < int(doubleSecond[0])):               	
                	adj = (doubleFirst[1],doubleSecond[0])
                else:                	
                	adj = (doubleSecond[0],doubleFirst[1])
                
                adjacencies[species].append(adj)
                
    return adjacencies
    
    
def read_SCJ_output(file):
	species_marker_order = {}
	species = ""
	f = open(file, "r")
	for line in f:
		if line.startswith(">"):
			if not species == "":
				species_marker_order[species] = chromosomes               
			species = line.rstrip("\n")[1:].split(" ")[0]
			chromosomes = {}
		elif line.startswith("#"):
			chrom = line.rstrip("\n")[1:]
		else:
                    order = line.rstrip("\n")[:-2].split(" ")
                    chromosomes[chrom] = order
        species_marker_order[species] = chromosomes
        
        
        f.close()
        return species_marker_order
        

def read_Hartigan_output(file):
	species_marker_order = {}
	species = file
	chromCounter = 0
	f = open(file, "r")
	chromosomes = {}
	for line in f:
			if not line == "" and not "Number" in line:
				order = line.rstrip("\n").split(" ")[:-1]
				chromosomes[chromCounter] = order
				chromCounter = chromCounter + 1
	species_marker_order[species] = chromosomes
	
	f.close()
	return species_marker_order
	
def read_Marker_file(marker):

    #print "Number of undoubled marker: "
    # read undoubled marker, for each species
    species_marker_order = {}
    file = open(marker, "r")
    species = ""
    for line in file:
        # new species
        if line.startswith(">"):
            if not species == "":
                species_marker_order[species] = chromosomes
                #print species
                #print markerCount
            species = line.split("\t")[0][1:].rstrip("\n")
            chromosomes = {}
            markerCount = 0
            # new chromosome
        elif line.startswith("#"):
            chrom = line.rstrip("\n")[2:]
        elif not line == "\n":
            order = line.rstrip("\n")[:-2].split(" ")
            markerCount = markerCount + len(order)
            chromosomes[chrom] = order
    species_marker_order[species] = chromosomes
    #print species
    #print markerCount
    file.close()
    return species_marker_order
	
	
	
fitch_adj = findAdjacencies(read_SCJ_output(fitchfile)) 	

hartigan_adj = findAdjacencies(read_Hartigan_output(hartiganfile)) 	
	
#ancestral_adj = findAdjacencies(read_Marker_file(ancestral)) 	
	
	
#compare hashes!

adjList_fitch = fitch_adj[fitch_adj.keys()[0]]
adjList_hartigan = hartigan_adj[hartigan_adj.keys()[0]]
elems_missing = []
correctCounter = 0
	
#elem_missing = adj only in fitch
for elem in adjList_fitch:
	if not elem in adjList_hartigan:
		elems_missing.append(elem)
	else:
		correctCounter = correctCounter + 1
		
	
#elem_wrong = adj only in hartigan
elems_wrong = []

for elem in adjList_hartigan:
	if not elem in adjList_fitch:
		elems_wrong.append(elem)

print "In both: "+str(correctCounter)+"\n"
print "Only in Fitch: "+str(len(elems_missing))+"\n"
print elems_missing
print "Only in Hartigan: "+str(len(elems_wrong))+"\n"
print elems_wrong

    
    	
# for spec in fitch_adj:
# 	correctCounter = 0
# 	adjList_anc = ancestral_adj[spec]
# 	
# 	elems_missing = []
# 	for elem in adjList_fitch:
# 		if not elem in adjList_anc:
# 			elems_missing.append(elem)
# 		else:
# 			correctCounter = correctCounter + 1
# 		
# 	
# 	elems_wrong = []
# 
# 	for elem in adjList_anc:
# 		if not elem in adjList_fitch:
# 			elems_wrong.append(elem)	
# 	
# 	print "Fitch: correct adjacencies "+str(correctCounter)+"\n"
# 	print "Fitch: wrong adjacencies "+str(len(elems_missing))+"\n"
# 	print "Fitch: missing adjacencies "+str(len(elems_wrong))+"\n"
# 	
# 	
# 	correctCounter = 0
# 	elems_missing = []
# 	for elem in adjList_hartigan:
# 		if not elem in adjList_anc:
# 			elems_missing.append(elem)
# 		else:
# 			correctCounter = correctCounter + 1
# 		
# 	
# 	elems_wrong = []
# 
# 	for elem in adjList_anc:
# 		if not elem in adjList_hartigan:
# 			elems_wrong.append(elem)	
# 	
# 	print "Hartigan: correct adjacencies "+str(correctCounter)+"\n"
# 	print "Hartigan: wrong adjacencies "+str(len(elems_missing))+"\n"
# 	print elems_missing
# 	print "Hartigan: missing adjacencies "+str(len(elems_wrong))+"\n"
# 	print elems_wrong
# 	
# 	
# 	
# 	
# 	
	
	
	
	
	