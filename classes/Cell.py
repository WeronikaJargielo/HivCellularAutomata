class Cell:

	### --- constructor of class Cell --- ###
	def __init__(self,**kwargs):
	   
		### --- cordinates and basic parametrs of the cell --- ###
		
		self.myX = kwargs.get('myX', -1)
		self.myY = kwargs.get('myY', -1)
		self.myZ = kwargs.get('myZ', -1)

		self.myState = 0 # at the beginning all cells are healthy
		self.newState = self.myState # newState is to update states of cells at the same time
		self.stateChanged = False

		self.numberOfI2Iterations = 0  # only infected cell type 2 

		### --- cell's neighbors --- ###
		self.wallMates = [] # list of the cell's neighbors which directly contact with the cell
		self.lineMates = [] # list of the cell's neighbors which touch the cell by line 
		self.pointMates = [] # list of the cell's neighbors which touch the cell by point (in the corners)


	### --- counting number of cell' neighbors in specific state --- ###
	def matesInSpecificState(self,listOfCell, specificState):
		states = [] # list of cell's neighbors' states
		for c in listOfCell:
			states.append(c.myState)
		return states.count(specificState)


	### --- checks if cell is a border cell in x, y, z sized world --- ###
	def checkIfBorder(self, xMax, yMax, zMax):
		return self.myX == 0 or self.myX == xMax or self.myY == 0 or self.myY == yMax or self.myZ == 0 or self.myZ == zMax


	### --- checks if cell is not on the other side of the world
	def checkIfNeighbouring(self, cell):
		return ((abs(self.myX - cell.myX) <= 1) and (abs(self.myY - cell.myY) <= 1) and (abs(self.myZ - cell.myZ) <= 1))


	def __repr__(self):
		return str(self.myState)

	
	### --- cell is true if it's not healthy --- ###
	def __bool__(self):
		return bool(self.myState)
