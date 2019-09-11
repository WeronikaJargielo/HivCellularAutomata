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
		self.wallMates = [] # list of the cell's neighbors which contact the cell by wall
		self.lineMates = [] # list of the cell's neighbors which touch the cell by line 
		self.pointMates = [] # list of the cell's neighbors which touch the cell by point (in the corners)
		self.displayWallMates = [] # list of cell's neigbors which touch the cell by wall directly

		### --- rules of game --- ###
		# Healthy Cell --> Infected type 1 (one of the rules) -> fromWhatTOWhat_whichStateCounts_whichTypeOfNeighbor
		self.healthyTOI1_I1_1N = 1 # min. 1 I1 cell
		self.healthyTOI1_I2_1N = 5 # min. 5 I2 cell
		self.healthyTOI1_I2_2N = 9 # min. 9 I2 cell
		self.healthyTOI1_I2_3N = 4 # min. 4 I2 cell
		# I1 --> I2 (next iteration)
		# I2 --> D (after next 2 iteration)
		# D --> I1 (with probability of infection)
		# D --> H (with probability of replenision - probability of infection)

		self.isBorderCell = False # True if cell is a border cell, needs to be set by World


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