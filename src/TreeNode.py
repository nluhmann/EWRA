#!/usr/bin/env python


#representation of a node in the tree
class TreeNode:
	
	#init
	def __init__(self, isSpecial, parent=None, weight=None, id=None):
		self.id = id
		self.children = []
		self.weight = weight
		self.parent = parent
		self.data = {}
		self.isLeave = False
		self.height = 0
		self.special = isSpecial
		self.oldWeight = 0
		
	
	
	#set data entry, e.g. bottom up annotation
	def addData(self, key, content):
		self.data[key] = content
	
	
	
	#get data entry
	def getData(self, key):
		if key in self.data:
			return self.data[key]
		else: 
			return None
	
	#get id
	def getID(self):
		return self.id
		
	def isSpecial(self):
		return self.special
	
	def getParent(self):
		return self.parent
	
	
	def getChildren(self):
		return self.children
		
	
	def getWeight(self):
		return self.weight
		
	def getOldWeight(self):
		if not self.oldWeight == 0:
			return self.oldWeight
		else:
			return self.weight
	
		
	def getParentAnnotation(self):
		return self.parent.getData("final")
		
	def isSpecial(self):
		return self.special
	
	def followPath(self):
		if(not self.getParent() == None):
			print self.getParent().getID()
			self.getParent().followPath()
			yield self
		yield self	
	

	def removeChild(self,child):
		#make sure that the child is in there
		assert child in self.children
		self.children.remove(child)
	
	
	
	#set label for tree	
	def setID(self, id):
		self.id = id
	
	#add a child of the current node
	def addChildren(self, node):
		#make sure that the child is not already in the child list
		assert node not in self.children
		self.children.append(node)
		#set this node as parent node also
		node.parent = self
	
	#set the weight of the edge to the parent of this node	
	def setWeight(self, weight):
		if not self.weight == None:
			self.oldWeight = self.weight
		self.weight = weight
		
	#set the parent node
	def setParent(self, parents):
		self.parent = parents
		
	#get all leaves under this node in the tree
	def getLeaves(self,x=None):
		if x == None:
			x = []
		#node is leaf itself: add to list
		if len(self.children) == 0:
			x.append(self)
		else:
			#find children that are leaves recursively
			for child in self.children:
				child.getLeaves(x)
				
		#return child list
		return x
		
		
		
	#get names of all leaves under this node in the tree	
	def getLeafNames(self, x=None):
		if x == None:
			x = []
		if len(self.children) == 0:
			x.append(self.id)
		else:
			for child in self.children:
				child.getLeafNames(x)
		return x
		
	
	
	#node iterator, preorder = bottom-up, postorder = top-down
	#returns generator (yield)	
	def iternodes(self,order="preorder"):
		if order.lower() == "preorder":
			yield self
		for child in self.children:
			for d in child.iternodes(order):
				yield d
		if order.lower() == "postorder":
			yield self
			
			
			
	def getNewickString(self,showbl=False):
		ret = ""
		for i in range(len(self.children)):
			if i == 0:
				ret += "("
			ret += self.children[i].getNewickString(showbl)
			if i == len(self.children)-1:
				ret += ")"
			else:
				ret += ","
		if self.id != None:
			ret += self.id
		if showbl == True:
			ret += ":" + str(self.weight)
		return ret