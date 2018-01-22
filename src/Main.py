#!/usr/bin/env python

import TreeReader
import Tree
import copy
import networkx as nx
import sys



tree = sys.argv[1]
allAdjacencies = sys.argv[2]
outputAdjacencies = sys.argv[3]
outputScaffolds = sys.argv[4]
if len(sys.argv) > 4:
	newWeight = sys.argv[5]
else:
	newWeight = 0




# 1. Read tree
treeString = open(tree).read().replace('\n', '')
tree = TreeReader.parse(treeString)
tree = TreeReader.annotateInternalNodes(tree)


# for j in tree.iternodes(order="preorder"):
# 	print j.getID()
# 	print j.getLeafNames()
# 	print "-------"


# 2. Rerooting & Attaching assembly graph leaf
newTree = Tree.reroot(tree, newWeight)
#Tree.printStructure(newTree)




# 3. read all_adjacencies line per line and annotate leaves of the tree with binary values
file = open(allAdjacencies, "r")
bottomUpTrees = {}
bottomUpTrees_s = {}
adjacencyCounter = 0
treeAdjacencies = []
for line in file:
	if ">" in line:
		splitted = line.split(" ")
		adjacency = splitted[0][1:]
		adjacencysplit = adjacency.split(",")
		first = adjacencysplit[0][1:]
		second = adjacencysplit[1][0:-1]
		tupel = (first,second)
		stati = splitted[1][1:-3].split(",")

		if stati[-1] == 1:
			print stati[-1]
		TreeCopy = copy.deepcopy(newTree)
		trees = Tree.annotateLeaves_Sankoff(TreeCopy, stati, speciesListe)
		bottomUptree = Tree.bottomUpLabeling_Sankoff(trees)
		bottomUpTrees[tupel] = bottomUptree
		adjacencyCounter = adjacencyCounter + 1
	else:
		speciesListe = line.replace('\n', '').split(",")	

print "Number of different adjacencies in total (adjacencies present in at least one leaf): ", adjacencyCounter





# 4. collect all adjacencies labeled 1 or 1,0 at root
C1Padjacencies = []
for adjacency in bottomUpTrees:
	tree = bottomUpTrees[adjacency]
	if tree.getData("C1") < tree.getData("C0"):
		C1Padjacencies.append(adjacency)
		

# build graph out of these adjacencies
G = nx.Graph()
for adjacency in C1Padjacencies:
	#for each adjacency, add two nodes
	G.add_node(adjacency[0])
	G.add_node(adjacency[1])
	#and an edge
	G.add_edge(adjacency[0],adjacency[1])
	
# select maximum matching on this graph, returns a set of adjacencies that are part of the max. card. matching
matching = nx.maximal_matching(G)
print "Number of adjacencies reconstructed for root before linearization: ", len(C1Padjacencies)
print "Number of adjacencies in matching: ", len(matching)
print "----------------------"

# set all adjacencies that are not part of the matching to 0 at root
countout = 0
for adjacency in C1Padjacencies:
	revadjacency = (adjacency[1],adjacency[0])
	if adjacency not in matching:
		if revadjacency not in matching:
			tree = bottomUpTrees[adjacency]
			if tree.getData("C1") < tree.getData("C0"):
				countout = countout + 1
				tree.addData("C1",float("inf"))
				bottomUpTrees[adjacency] = tree



# 5. compute top-down labeling
for adjacency in bottomUpTrees:
	tree = bottomUpTrees[adjacency]
	bottomUpTrees[adjacency] = Tree.topDownLabeling_Sankoff(tree)




# 6. for each internal node, collect adjacencies
speciesHash = {}
for adjacency in bottomUpTrees:
	if adjacency[0] != adjacency[1]:
		tree = bottomUpTrees[adjacency]
		for j in tree.iternodes(order="postorder"):
			if len(j.getChildren()) != 0:
				if j.getData("final_s") == 1:
					if j.getID() in speciesHash:
						speciesHash[j.getID()][adjacency[0]] = adjacency[1]
						speciesHash[j.getID()][adjacency[1]] = adjacency[0]
					else:	
						hash = {}
						hash[adjacency[0]] = adjacency[1]
						hash[adjacency[1]] = adjacency[0]
						speciesHash[j.getID()] = hash





def otherExtremity(extrem):
	extrem = int(extrem)
	if extrem % 2 == 0:
		return extrem -1
	elif extrem % 2 == 1:
		return extrem +1


### test test test
# for node in speciesHash:
# 	adjacencyHash = speciesHash[node]
# 	print adjacencyHash
# 	for extremity in adjacencyHash:
# 		other = otherExtremity(extremity)
# 		if str(other) in adjacencyHash:
# 			print "yes"
# 		else: 
# 			print "no"

# 7. for each internal node, create file and output all adjacencies
for node in speciesHash:
	adjacencyHash = speciesHash[node]
	path = outputAdjacencies+node
	file = open(path, "w")
	for elem in adjacencyHash:
		next = adjacencyHash[elem]
		file.write(elem+" -> "+next+"\n")
	file.close()



for node in speciesHash:
	adjacencyHash = speciesHash[node]
	for elem in adjacencyHash:
		neighbor = adjacencyHash[elem]
		if not adjacencyHash[neighbor] == elem:
			print node
			print elem
			print neighbor
			print adjacencyHash[neighbor]
			print "------------"

# 8. for each internal node, output scaffolds
scaffolds = {}
for node in speciesHash:
	adjacencyHash = speciesHash[node]
	for elem in adjacencyHash.keys():
		if elem in adjacencyHash:
			scaffold = ""
			neighbor = adjacencyHash[elem]
			del adjacencyHash[elem]
			if neighbor in adjacencyHash:
				del adjacencyHash[neighbor]
			#extend adjacency to the left
			scaffold = ""+elem
			bool = True
			while bool == True:
				next = str(otherExtremity(elem))
				scaffold = str(next) +" "+ scaffold
				if next in adjacencyHash:
					elem = adjacencyHash[next]
					#remove this adjacency from hash
					if elem in adjacencyHash:
						del adjacencyHash[elem]
					del adjacencyHash[next]
					scaffold = str(elem) +" "+ scaffold
				else:
					bool = False
			#extend adjacency to the right
			scaffold = scaffold +" "+ neighbor
			bool = True
			while bool:
				next = str(otherExtremity(neighbor))
				scaffold = scaffold +" "+ str(next)
				if next in adjacencyHash:
					neighbor = adjacencyHash[next]
					#remove this adjacency from hash
					if neighbor in adjacencyHash:
						del adjacencyHash[neighbor]
					del adjacencyHash[next]
					scaffold = scaffold +" "+ str(neighbor)
				else:
					bool = False
			
			if node in scaffolds:
				scaffolds[node].append(scaffold)
			else:
				liste = []
				liste.append(scaffold)
				scaffolds[node] = liste	
					
# 9. undouble scaffolds
undoubledScaffolds = {}
numberOfMarker = {}
for node in scaffolds:
	for scaffold in scaffolds[node]:
		markerCounter = 0
		undoubledScaffold = ""
		array = scaffold.split(' ')
		for i in range(0, len(array), 2):
			first = int(array[i])
			second = int(array[i+1])
			markerCounter = markerCounter +1
			if first - second == 1:
				marker = str(first / 2)
				marker = "-"+marker
				undoubledScaffold = undoubledScaffold + marker + " "
			elif second - first == 1:
				marker = str(second / 2)
				marker = "+"+marker
				undoubledScaffold = undoubledScaffold + marker + " "
			else:
				print "error" 
			
		if node in undoubledScaffolds:
			undoubledScaffolds[node].append(undoubledScaffold)
		else:
			liste = []
			liste.append(undoubledScaffold)
			undoubledScaffolds[node] = liste	
		if node in numberOfMarker:
			number = numberOfMarker[node]
			new = number + markerCounter
			numberOfMarker[node] = new
		else:
			numberOfMarker[node] = markerCounter
	
# 10. output scaffolds
for node in undoubledScaffolds:
	scaffoldArray = undoubledScaffolds[node]
	path = outputScaffolds+node
	file = open(path, "w")
	for elem in scaffoldArray:
		file.write(elem+"\n")
	file.write("\n")
	file.write("Number of marker: ")
	file.write(str(numberOfMarker[node]))
	file.close()	
