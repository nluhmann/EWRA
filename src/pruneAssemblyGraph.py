#!/usr/bin/env python


#######
#remove contigs from the graph that are too short
#######



import sys

dotfile = sys.argv[1]
filename = sys.argv[2]
biggestContigID = int(sys.argv[3])
outfile = sys.argv[4]


print "read contig IDs"
file = open(filename, "r")
bigContigsList = [int(x.strip('\n')) for x in file.readlines()] # read all lines to list
file.close()



contigsList = [i for i in range(biggestContigID+1)]





# two hashes for the graph, value is list of nodes either following or preceding key node
# list of nodes following key node
following = {}
# list of nodes preceding key node
preceeding = {}


print "read dot file"
file = open(dotfile, "r")
for line in file:
	if "->" in line: 
		array = line.split('"')
		start = array[1]
		stop = array[3]
		if start in following:
			liste = following[start]
			if stop not in liste:
				liste.append(stop)
			following[start] = liste
		else:
			liste = []
			liste.append(stop)
			following[start] = liste
		if stop in preceeding:
			liste = preceeding[stop]
			if start not in liste:
				liste.append(start)
			preceeding[stop] = liste
		else:
			liste = []
			liste.append(start)
			preceeding[stop] = liste


file.close()

print "number of entrys following", len(following)
print "number of entrys preceeding", len(preceeding)


#find the ID of all contigs that are too short
s = set(bigContigsList)
shortContigs = [x for x in contigsList if x not in s]

#for each contig that is too short, connect preceding and following contigs in the graph
for contig in shortContigs:	
	plusContig = str(contig).rstrip('\r\n') + "+"
	minusContig = str(contig).rstrip('\r\n') + "-"
	follower = []
	predecessor = []
	
	
	#first direction (plus -> minus)
	if plusContig in following:
		fol = following[plusContig]
		follower = list(set(fol))
	if minusContig in preceeding:
		pred = preceeding[minusContig]
		predecessor = list(set(pred))

	

	
	#extremity cannot follow or preced itself	
	if plusContig in follower:
		follower.remove(plusContig)
	if minusContig in predecessor:
		predecessor.remove(minusContig)
	
	
#okay, connect:
	#if one of the lists is empty, nothing needs to be connected
	if len(follower) is 0 or len(predecessor) is 0:
		if plusContig in following:
			del following[plusContig]
		if minusContig in preceeding:
			del preceeding[minusContig]
	
	if len(follower) > 0 and len(predecessor) > 0:
 		for pred in predecessor:
 			liste = following[pred] 			
 			newliste = list(set(follower) | set(liste))
 			newliste.remove(minusContig)
 			following[pred] = newliste
 		for foll in follower:
 			liste = preceeding[foll]
 			newliste = list(set(predecessor) | set(liste))
 			newliste.remove(plusContig)
 			preceeding[foll] = newliste
	
	
	follower = []
	predecessor = []
	
	
	#other direction (minus -> plus)#
	if minusContig in following:
		fol = following[minusContig]
		follower = list(set(fol))
	if plusContig in preceeding:
		pred = preceeding[plusContig]
		predecessor = list(set(pred))
		
		

	#extremity cannot follow or preced itself	
	if minusContig in follower:
		follower.remove(minusContig)
	if plusContig in predecessor:
		predecessor.remove(plusContig)


	#if one of the lists is empty, nothing needs to be connected
	if len(follower) is 0 or len(predecessor) is 0:
		if minusContig in following:
			del following[minusContig]
		if plusContig in preceeding:
			del preceeding[plusContig]
	
	if len(follower) > 0 and len(predecessor) > 0:
		for pred in predecessor:
			liste = following[pred]			
			newliste = list(set(follower) | set(liste))
			newliste.remove(plusContig)
			following[pred] = newliste
		for foll in follower:
			liste = preceeding[foll]			
			newliste = list(set(predecessor) | set(liste))
			newliste.remove(minusContig)
			preceeding[foll] = newliste
	
	
	
	#remove plus and minus contigs from both hashes
	if plusContig in following:
		del following[plusContig]
	if minusContig in following:
		del following[minusContig]
	if plusContig in preceeding:
		del preceeding[plusContig]
	if minusContig in preceeding:
		del preceeding[minusContig]
	

	
	
#print out pruned graph in dot format:
file = open(outfile, "w")
file.write("digraph adj {\n")
file.write("graph [k=21]\n")
file.write("edge [d=-20]\n")

### first part ###
for contig in bigContigsList:
	plusContig = str(contig).rstrip('\r\n') + "+"
	minusContig = str(contig).rstrip('\r\n') + "-"
	file.write('"'+plusContig+'"'+"\n")
	file.write('"'+minusContig+'"'+"\n")

### second part ###
for contig in bigContigsList:
	plusContig = str(contig).rstrip('\r\n') + "+"
	minusContig = str(contig).rstrip('\r\n') + "-"		
	if plusContig in following:
		follower = following[plusContig]
		#check
		for foll in follower:
			liste = preceeding[foll]
			if not plusContig in liste:
				print "error"
			file.write('"'+plusContig+'"'+' '+'->'+' '+'"'+foll+'"'+"\n")
	if minusContig in following:
		follower = following[minusContig]
		for foll in follower:
			liste = preceeding[foll]
			if not minusContig in liste:
				print "error"
			file.write(	'"'+minusContig+'"'+' '+'->'+' '+'"'+foll+'"'+"\n")	
			
			
			
file.close()	
	
	

	
	
	
	
	
	
	