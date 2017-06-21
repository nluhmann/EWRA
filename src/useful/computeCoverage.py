#!/usr/bin/env python

import sys

markerfile import sys
families = sys.argv[2]

file = open(markerfile, "r")
markerset = []
for line in file:
	if len(line) != 0:
		if line[0] != "N":
			array = line.replace('\n', '').split(' ')
			markerset.extend(array)
file.close()


familyHash = {}
filef = open(families, "r")
for line in filef:
	if line.startswith('>'):
		id = line[1:].replace('\n', '')
	elif len(line) > 1:
		array = line.split(':')
		pos = array[2].split('-')
		length = abs(int(pos[1])-int(pos[0]))
		familyHash[id] = length
filef.close()

lengthCounter = 0

for marker in markerset:
	if marker != '':
		length = familyHash[marker[1:]]
		lengthCounter = lengthCounter + length


print "Total marker length: "+str(lengthCounter)	