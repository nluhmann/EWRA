#!/usr/bin/env python

import sys

#contig file from assembly
filename = sys.argv[1]

#outfile for filtered contigs
outfile = sys.argv[2]

#min number of bp
limit = sys.argv[3]


#contig length file
ancientContigLengthFile = sys.argv[4]

contiglist = []
contiglengths = []
totalLength = 0
file = open(filename, "r")
secondLine = False
for line in file:
	if secondLine:
		array = firstLine.split(' ')
		if int(array[1]) >= int(limit):
			contiglist.append(firstLine)
			contiglist.append(line)
			lengthformat = firstLine.replace('\n', '')+" length "+array[1]+'\n'
			totalLength = totalLength + int(array[1])
			contiglengths.append(lengthformat)
		secondLine = False
	else:
		firstLine = line
		secondLine = True
file.close()
  

  
file = open(outfile, "w")
for item in contiglist:
	file.write(item)
file.close()

file = open(ancientContigLengthFile, "w")
for item in contiglengths:
		file.write(item)
file.close()

print "Contigs greater "+limit+" cover "+str(totalLength)+"bp."