class Cell:

	### --- constructor of class Cell --- ###
	def __init__(self,**kwargs):
	   
		### --- cordinates and basic parametrs of the cell --- ###
		self.myX = kwargs.get('myX', -1)
		self.myY = kwargs.get('myY', -1)
		self.myZ = kwargs.get('myZ', -1)

		self.myState = kwargs.get('myState', 0) # at the beginning all cells are healthy
		self.newState = self.myState # newState is to update states of cells at the same time

		self.numberOfI1Iterations = 1
		self.numberOfI2Iterations = 1
		self.isBorderCell = True

		### --- cell's neighbors --- ###
		self.wallMates = [] # list of the cell's neighbors which directly contact with the cell
		self.lineMates = [] # list of the cell's neighbors which touch the cell by line 
		self.pointMates = [] # list of the cell's neighbors which touch the cell by point (in the corners)


	### --- counting number of cell's neighbors in specific state --- ###
	def numberOfMatesInSpecificState(self, listOfCells, specificState):
		states = 0 # list of cell's neighbors' states
		for cell in listOfCells:
			if cell.myState == specificState:
				states = states + 1
		return states


	### --- checks if cell is a border cell in x, y, z sized world --- ###
	def setIsBorderCell(self, xMax, yMax, zMax):
		self.isBorderCell = (self.myX == 0 or self.myX == xMax - 1
							or self.myY == 0 or self.myY == yMax - 1
							or self.myZ == 0 or self.myZ == zMax - 1)


	### --- for printing cell --- ###
	def __repr__(self):
		return str(self.myState)


	### --- cell is true if it's not healthy --- ###
	def __bool__(self):
		return bool(self.myState)
