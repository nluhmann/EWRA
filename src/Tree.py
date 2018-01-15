#!/usr/bin/env python

import TreeReader
from TreeNode import TreeNode


def annotateLeaves(tree):
	annotations = { "A": [0], "B": [1], "C": [1], "D": [0], "E": [1], "F": [0]}
	children = tree.getLeaves()
	for child in children:
		id = child.getID()
		child.addData("bottom",annotations[id])

def annotateLeaves(tree, liste, speciesliste):
	children = tree.getLeaves()
	counter = 0
	for child in children:
		id = child.getID()
		child.addData("bottom", [int(liste[speciesliste.index(id)])])
	return tree	
	
def annotateLeaves_Sankoff(tree, liste, speciesliste):
	children = tree.getLeaves()
	counter = 0
	for child in children:
		id = child.getID()
		anno = int(liste[speciesliste.index(id)])
		if anno == 1:
			child.addData("C1",0)
			child.addData("C0",float("inf"))
		else:
			child.addData("C0",0)
			child.addData("C1",float("inf"))
	return tree

def testAnnotation(tree):
	for j in tree.iternodes(order="postorder"):
		print j.getID()
		print j.getWeight()
		#print j.getData("bottom")
		




def printSpecial(tree):
	for j in tree.iternodes(order="postorder"):
		if j.isSpecial():
			print j.getID()





def bottomUpLabeling_Sankoff(tree):
	for node in tree.iternodes(order="postorder"):
	
		#get annotation for all children of node
		if node.getData("C1") == None:
			C1 = 0
			C0 = 0
            
			children = node.getChildren()
			for child in children:
				weight = 1/float(child.getWeight())
				C1_child = child.getData("C1")
				C0_child = child.getData("C0")
            	#update C1
				if C0_child + weight < C1_child:
					C1 += C0_child + weight
				else:
					C1 += C1_child
            	
            	#update C0
				if C1_child + weight < C0_child:
					C0 += C1_child + weight
				else:
					C0 += C0_child
			node.addData("C1",C1)
			node.addData("C0",C0)           
	return tree
    

def topDownLabeling_Sankoff(tree):
	root = True
	for node in tree.iternodes(order="preorder"):	
		if root:			
			if node.getData("C1") < node.getData("C0"):
				node.addData("final_s",1)
			else:
				node.addData("final_s",0)
			root = False
		else:
			parentAssignment = node.getParentAnnotation()
			weight = 1/float(node.getWeight())
			if parentAssignment == 1:
				cost1 = node.getData("C1")
				cost0 = node.getData("C0") + weight
			else:
				cost1 = node.getData("C1") + weight
				cost0 = node.getData("C0")
			if cost1 < cost0:
				node.addData("final_s",1)
			else:
				node.addData("final_s",0)
	return tree



	
	
def testTopDown(tree):
	for j in tree.iternodes(order="postorder"):
		print j.getID()
		print j.getData("final")
	



def reroot(tree):
	#remove old root and join edges
	children = tree.getChildren()
	
	#find special node
	for j in tree.iternodes(order="preorder"):
		if j.isSpecial():
			
			node = j.getParent()
			save = node
			path = []
			path.append(node)
			while (not node.getParent() == None):
				parent = node.getParent()
				path.append(parent)
				node = parent

				
			for index in range(len(path)):	
				if not index == 0:
					path[index-1].addChildren(path[index])
				if not index == len(path)-1:
					path[index+1].setWeight(path[index].getOldWeight())
					path[index+1].setParent(path[index])
					path[index+1].removeChild(path[index])
					
				
		

			newRoot = splitEdge(save,j)
			
			#remove all nodes that have only one child
			for j in newRoot.iternodes(order="postorder"):
				children = j.getChildren()
				if len(children) == 1:
					if j.getParent():
						child = children[0]
						parent = j.getParent()
						childWeight = child.getWeight()
						parentWeight = j.getWeight()
						newWeight = float(childWeight) + float(parentWeight)
						
						parent.removeChild(j)
						parent.addChildren(child)
						child.setParent(parent)
						child.setWeight(newWeight)
			
			
			
	return newRoot
	
def rerootAtNode(tree):
	#remove old root and join edges
	children = tree.getChildren()
	
	#find special node
	for j in tree.iternodes(order="preorder"):
		if j.isSpecial():
			#print j.getID()
			#juhu wir haben die neue wurzel gefunden
			node = j
			#save = node
			#erstmal alle Knoten auf dem Pfad zur Wurzel einsammeln
			#path = liste mit allen knoten von special bis wurzel, wurzel ist letzter knoten
			path = []
			path.append(node)
			while (not node.getParent() == None):
				parent = node.getParent()
				path.append(parent)
				node = parent
			
				
			for index in range(len(path)):	
				if not index == 0:
					path[index-1].addChildren(path[index])
				if not index == len(path)-1:
					path[index+1].setWeight(path[index].getOldWeight())
					path[index+1].setParent(path[index])
					path[index+1].removeChild(path[index])
				
		
			
			newRoot = j
			
			
			#remove all nodes that have only one child
			for j in newRoot.iternodes(order="postorder"):
				children = j.getChildren()
				if len(children) == 1:
					if j.getParent():
						child = children[0]
						parent = j.getParent()
						childWeight = child.getWeight()
						parentWeight = j.getWeight()
						newWeight = float(childWeight) + float(parentWeight)
						
						parent.removeChild(j)
						parent.addChildren(child)
						child.setParent(parent)
						child.setWeight(newWeight)
			
			

	return newRoot	

def addLeaf(newRoot):
	newLeaf = TreeNode(True)
	newLeaf.setParent(newRoot)
	newLeaf.setID("AssemblyGraphLeaf")
	newLeaf.setWeight(computeLeafEdgeWeight(newRoot))
	newRoot.addChildren(newLeaf)
	return newRoot	

#split the edge at which the new root should be created, split edge weight for two new outgoing edges
def splitEdge(parentNode, childNode):
	edgeWeight = childNode.getWeight()
	newRoot = TreeNode(True)
	newRoot.setID("root")
	newRoot.addChildren(parentNode)
	newRoot.addChildren(childNode)
	parentNode.setParent(newRoot)
	childNode.setParent(newRoot)
	parentNode.removeChild(childNode)
	#split edge weight, by half for example (fuers erste)
	first = float(edgeWeight)/2
	second = float(first)/2
	left = first + second
	parentNode.setWeight(second)
	childNode.setWeight(left)
	#add new leaf representing assembly graph
	newLeaf = TreeNode(True)
	newLeaf.setParent(newRoot)
	newLeaf.setID("AssemblyGraphLeaf")
	newLeaf.setWeight(computeLeafEdgeWeight(newRoot))
	newRoot.addChildren(newLeaf)
	return newRoot	



def computeLeafEdgeWeight(tree):
#TODO: make better
	return 0.01


def printStructure(tree):
	for j in tree.iternodes(order="postorder"):
		print "ID", j.getID()
		print "length", j.getWeight()
		children = j.getChildren()
		for child in children:
			print "Child", child.getID()
		if not j.getParent() == None:
			print "Parent", j.getParent().getID()
		print "------------"



	
	
	
	
	
	
	
	
	
	
