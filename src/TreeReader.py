#!/usr/bin/env python

from TreeNode import TreeNode
import string
import pdb



"""
the reader takes a tree in Newick format,
builds all the nodes and edges and 
returns the root node
format: "(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);"
"""



#return root node of the tree
def parse(string):
	node2 = TreeNode(False)
	return build(string, node2, 0, len(string), 1)
	
	
#IdCounter = 0	
	
def build(string, parentNode, start, stop, index):
	if(not string[start] == "("):
		id = string[start:stop]
		parentNode.setID(id)
		return parentNode
	
	b = 0 #bracket counter
	c = 0 #colon counter
	x = start #position marker
	
	
	for i in range(start, stop):
		char = string[i]
		if(not char == ";"):
			if(char == "("):
				b = b+1
			elif(char == ")"):
				b = b-1
			elif(char == ':'):
				c = i
		
			if(b == 0 or b == 1 and char == ","):
				if string[c-1] == "@":
					parentNode.addChildren(build(string, TreeNode(True,parentNode,string[c+1:i],"ancient"), x+1, c-1, index))
				else:
					parentNode.addChildren(build(string, TreeNode(False,parentNode,string[c+1:i],""), x+1, c, index))
				x = i

	return parentNode
	

def annotateInternalNodes(tree):
	IDCounter = 0
	for j in tree.iternodes(order="postorder"):
		
		if j.getID() == "" or j.getID() == None: 
			j.setID(str(IDCounter))
			IDCounter = IDCounter + 1
	return tree	
	
# testree = "(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);"
# test = parse(testree)
# tree = annotateInternalNodes(test)
# print test.getLeafNames()
# print test.getNewickString(True)
# for j in tree.iternodes(order="postorder"):
#  		if len(j.getChildren()) == 0:
#  			print j.getID()
#  		else:
#  			print j.getID()

# test2 = "((((One:0.2,Two:0.3):0.3,(Three:0.5,Four:0.3):0.2):0.3,Five:0.7):0.0);"
# test = parse(test2)
# print test.getLeafNames()
# print test.getNewickString(True)