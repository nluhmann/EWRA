import sys
import re

treefile = sys.argv[1]
markerfile = sys.argv[2]
outfile = sys.argv[3]




# double marker id to account for orientation
def doubleMarker(marker):
    if "-" in marker:
        return int(marker[1:]) * 2, (int(marker[1:]) * 2) - 1
    else:
        return (int(marker) * 2) - 1, int(marker) * 2
        
        
# double marker and find adjacencies in chromosomes
def findAdjacencies(speciesHash):
    print "collect extant adjacencies from marker file..."
    # keys: (left marker, right marker), value: [(species,chromosome),...]
    adjacencies = {}
    for species in speciesHash:
        chromosomes = speciesHash[species]
        for chrom in chromosomes:
            orderList = chromosomes[chrom]
            for i in range(0,len(orderList)-1):
                first = orderList[i]
                second = orderList[i+1]
                doubleFirst = doubleMarker(first)
                doubleSecond = doubleMarker(second)
                #take right extrem of first and left extrem of second for adj tuple
                adj = (doubleFirst[1],doubleSecond[0])
                rev = (doubleSecond[0],doubleFirst[1])
                if adj in adjacencies:
                    adjacencies[adj].append(species)
                elif rev in adjacencies:
                    adjacencies[rev].append(species)
                else:
                    adjacencies[adj] = [species]
    return adjacencies
    
    
def read_Marker_file(marker):
 #compute adjacencies, compute weights with DeClone

    print "Number of undoubled marker: "
    # read undoubled marker, for each species
    species_marker_order = {}
    file = open(marker, "r")
    species = ""
    for line in file:
        # new species
        if line.startswith(">"):
            if not species == "":
                species_marker_order[species] = chromosomes
                print species
                print markerCount
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
    print species
    print markerCount
    file.close()
    return species_marker_order
    


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
	
species = readSpeciesTree(treefile)
adjacencies = findAdjacencies(read_Marker_file(markerfile))


out = open(outfile,"w")
out.write(",".join(species)+"\n")
for adj in adjacencies:
	indicator = []
	for spec in species:
		if spec in adjacencies[adj]:
			indicator.append('1')
		else:
			indicator.append('0')
	out.write(">("+str(adj[0])+","+str(adj[1])+") "+"["+",".join(indicator)+",]\n")

out.close()





