import sys

bsbfile = sys.argv[1]

fpsacfile = sys.argv[2]

fitchfile = sys.argv[3]

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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False




def read_ANGES_output(file):
	species_marker_order = {}
	species = file
	f = open(file, "r")
	chromosomes = {}
	for line in f:
		if line.startswith("#"):
			chrom = line.rstrip("\n")[1:]
		elif line.startswith(">"):
			species = line.rstrip("\n")[1:]
		else:
			#remove _Q and T from beginning and end of marker order!
			order = line.rstrip("\n").split(" ")
			newOrder = []
			for elem in order:
				if is_number(elem):
					newOrder.append(elem)
            		chromosomes[chrom] = newOrder
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
	




bsb_adj = findAdjacencies(read_Hartigan_output(bsbfile)) 	

fpsac_adj = findAdjacencies(read_ANGES_output(fpsacfile)) 	

fitch_adj = findAdjacencies(read_SCJ_output(fitchfile)) 


#compare hashes!

adjList_fpsac = fpsac_adj[fpsac_adj.keys()[0]]
adjList_hartigan = bsb_adj[bsb_adj.keys()[0]]
adjList_fitch = fitch_adj[fitch_adj.keys()[0]]


all = []
fpsachartigan = []
fpsacfitch = []
fitchhartigan = []
fpsac = []
hartigan = []
fitch = []

for elem in adjList_fpsac:
	if elem in adjList_hartigan and elem in adjList_fitch:
		all.append(elem)
	elif elem in adjList_hartigan:
		fpsachartigan.append(elem)
	elif elem in adjList_fitch:
		fpsacfitch.append(elem)
	else:
		fpsac.append(elem)

for elem in adjList_hartigan:
	if elem in adjList_fitch and not elem in adjList_fpsac:
		fitchhartigan.append(elem)
	elif elem not in adjList_fitch and elem not in adjList_fpsac:
		hartigan.append(elem)

for elem in adjList_fitch:
	if not elem in adjList_hartigan and not elem in adjList_fpsac:
		fitch.append(elem)


print "All: "+str(len(all))+"\n"
print "FPSAC - Hartigan: "+str(len(fpsachartigan))+"\n"
print fpsachartigan
print "FPSAC - Fitch: "+str(len(fpsacfitch))+"\n"
print fpsacfitch
print "Fitch - Hartigan: "+str(len(fitchhartigan))+"\n"
print fitchhartigan
print "FPSAC: "+str(len(fpsac))+"\n"
print fpsac
print "Hartigan: "+str(len(hartigan))+"\n"
print hartigan
print "Fitch: "+str(len(fitch))+"\n"
print fitch








# elems_missing = []
# correctCounter = 0
# 	
# #elem_missing = adj only in fitch
# for elem in adjList_fpsac:
# 	if not elem in adjList_hartigan:
# 		elems_missing.append(elem)
# 	else:
# 		correctCounter = correctCounter + 1
# 		
# 	
# #elem_wrong = adj only in hartigan
# elems_wrong = []
# 
# for elem in adjList_hartigan:
# 	if not elem in adjList_fpsac:
# 		elems_wrong.append(elem)
# 
# print "In both: "+str(correctCounter)+"\n"
# print "Only in FPSAC: "+str(len(elems_missing))+"\n"
# print elems_missing
# print "Only in Hartigan: "+str(len(elems_wrong))+"\n"
# print elems_wrong
# 	






















