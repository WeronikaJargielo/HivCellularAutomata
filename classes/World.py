from classes.Cell import *
from classes.Probability import *
# from classes.Visualisation import *
from classes.VisualisationVol2 import *
import random
from time import sleep
from _thread import start_new_thread

class World:
	### --- constructor of class World --- ###
	# kwargs.get('nameOfParametr', defaultValue)
	def __init__(self,**kwargs):

		### --- simulation parametrs --- ###
		self.rows = kwargs.get('rows', 100) # numbers of rows - x
		self.cols = kwargs.get('cols', 100) # numbers of cols - y
		self.layers = kwargs.get('layers', 100) # numbers of layers - z
		self.numberOfSimulation = kwargs.get('numberOfSimiulation', -1) # need in filename duriing saving to file
		self.dimension = self.rows * self.cols * self.layers # dimension of whole grid
		self.numberOfIterations = kwargs.get('numberOfIterations', 30) # numbers of iterations of simulation
		
		### --- states --- ###
		self.healthy = 0
		self.infected1 = 1
		self.infected2 = 2
		self.dead = 3
		
		self.numberOfIterationsInI2State = 2
		
		### --- Initial coditions --- ###
		# the probability/percentage of initial healthy cell infected by HIV 
		self.pInitialHIV = kwargs.get('pInitialHIV', 0.0005) # from Alive to I1

		# probability that a DEAD cell is replenished by an HEALTHY cell 
		self.pReplenision = Probability(nominator = 99 , denominator = 100) # from Dead to Alive

		# probability that a DEAD cell becomes a HEALTHY cell
		self.pInfection = Probability(nominator = 974 , denominator = 100000000) # from Dead to I1

		# make common denominator
		self.pInfection.commonDenominator(self.pReplenision)

		# initial number of cells of type infected 1
		self.numberOfI1Cell = kwargs.get('numberOfInfected_1_Cell', (self.dimension * self.pInitialHIV)) 
   
		self.cellsList = [] 
		self.createWorld() # creation of 3D grid of cells
		self.setStateOfIntialI1Cell(self.numberOfI1Cell) # setting the state of I1 cells randomly selected
		self.setCellsMates() # setting neighbours of each cell
	

	### --- creation of the world --- ###
	def createWorld(self): # creates the whole grid of cells
		for l in range(self.layers):
			singleLayer = []
			for r in range(self.rows): # loop creating list of cells
				singleRow = []
				for c in range(self.cols):
					cell = Cell(myX = r, myY = c, myZ = l)
					singleRow.append(cell)

				singleLayer.append(singleRow)

			self.cellsList.append(singleLayer)


	### --- setting inially infected 1 cells --- ###
	def setStateOfIntialI1Cell(self, numberOfI1Cell): 
		counter = 0
		while counter < self.numberOfI1Cell:

			setX = random.randrange(0, self.rows) 
			setY = random.randrange(0, self.cols)
			setZ = random.randrange(0, self.layers)

			if self.cellsList[setZ][setX][setY].myState != self.infected1:

				self.cellsList[setZ][setX][setY].myState = self.infected1
				self.cellsList[setZ][setX][setY].newState = self.infected1
				counter = counter + 1


	### --- finding out the state of particular cell --- ###
	def findOutStateOfCell(self, cell):
		# HEALTHY --> INFECTED 1
		if cell.myState == self.healthy: 
			
			if (	cell.matesInSpecificState(cell.wallMates, self.infected1) >= 1 # I1 cell, wall neighborhood
				 or cell.matesInSpecificState(cell.lineMates, self.infected1) >= 1 # I1 cell, line neighborhood
				 or (
						cell.matesInSpecificState(cell.wallMates, self.infected2) >= 5 # I2 cell, wall neighborhood
					and cell.matesInSpecificState(cell.lineMates, self.infected2) >= 9 # I2 cell, line neighborhood
					and cell.matesInSpecificState(cell.pointMates, self.infected2) >= 4 # I2 cell, point neighborhood
					)
				):
				
				cell.newState = self.infected1 
				cell.stateChanged = True

		# INFECTED 1 --> INFECTED 2
		elif cell.myState == self.infected1: 
			cell.newState = self.infected2
			cell.stateChanged = True
			cell.numberOfI2Iterations = 1

		# INFECTED 2 --> DEAD
		elif cell.myState == self.infected2:
			if cell.numberOfI2Iterations == self.numberOfIterationsInI2State:
				cell.newState = self.dead
				# cell.numberOfI2Iterations = 0  does not need, because setting cell.numberOfI2Iterations = 1 in block I1 -> I2
				# before cell comes to I2 state it needs to come through I1 state
				cell.stateChanged = True
			else:
				cell.numberOfI2Iterations = cell.numberOfI2Iterations + 1

		elif cell.myState == self.dead:
			randomProbability = random.randrange(0, self.pInfection.denominator)
			
			# DEAD --> INFECTED 1
			if randomProbability < self.pInfection.nominator:
				cell.newState = self.infected1
				cell.stateChanged = True

			# DEAD --> HEALTHY
			elif randomProbability < self.pReplenision.nominator: # (Prep-Pinf) remaining probability
				cell.newState = self.healthy
				cell.stateChanged = True


	### --- setting cell's neighbours --- ###
	def setCellsMates(self):

		wallNeighbors = 1
		lineNeighbors = 2
		pointNeighbors = 3

		for l in range(self.layers):
			for r in range(self.rows):
				for c in range(self.cols):
					cell = self.cellsList[l][r][c] # specific cell to 

					lRange = list(range(l-1, l+2))  # create range [first, last)
					rRange = list(range(r-1, r+2))
					cRange = list(range(c-1, c+2))

					if l+1 == self.layers: # sprawdzenie czy nie wychodzi poza zakres
						lRange[2] = 0   
					if r+1 == self.rows:
						rRange[2] = 0  
					if c+1 == self.cols:
						cRange[2] = 0  

					
					for ll in lRange:
						for rr in rRange:
							for cc in cRange:
								neighbourCell = self.cellsList[ll][rr][cc] 
								diffrentIndexes = (ll != cell.myZ) + (rr != cell.myX) + (cc != cell.myY)
								if diffrentIndexes == pointNeighbors:
									cell.pointMates.append(neighbourCell)
								elif diffrentIndexes == lineNeighbors:
									cell.lineMates.append(neighbourCell)
								elif diffrentIndexes == wallNeighbors:
									cell.wallMates.append(neighbourCell)


	### --- simulation of world --- ###
	def simulateWorld(self):
		# visualisation = Visualisation(cellsNumberInAxis = self.rows)
		visualisation = VisualisationVol2(cellsNumberInAxis = self.rows)
		
		try:
			start_new_thread(self.performSimulation, (visualisation, ))
		except:
			print("Unable to start thread")

		visualisation.startDisplayingWorld(self.cellsList)


	def performSimulation(self, visualisation):
		sleep(1)
		for i in range(self.numberOfIterations): # number of iteration
			for l in range(self.layers):
				for r in range(self.rows):
					for c in range(self.cols):

						cell = self.cellsList[l][r][c]  # single cell	
						cell.stateChanged = False # reset change info
						
						self.findOutStateOfCell(cell) # find out new state of cell
						
			for ll in range(self.layers):
				for rr in range(self.rows): # loops to update states of all cells at once
					for cc in range(self.cols):
						cell = self.cellsList[ll][rr][cc]  # single cell
						if cell.stateChanged == True:
							cell.myState = cell.newState # update cell.state of cell
							visualisation.refreshDisplay()

			print(self.countCellsInSpecificState())
			sleep(1)

		
	def printWorld(self):
		print("")
		for i in self.cellsList:
			print("layer")
			for j in i:
				print(j)


	### --- counting the cells in particular state on the grid --- ###
	def countCellsInSpecificState(self):
		stateCounter = [0, 0, 0, 0] # H, I1, I2, D
		for l in range(self.layers):
			for r in range(self.rows):
				for c in range(self.cols):
					cell = self.cellsList[l][r][c]
					stateCounter[cell.myState] =  stateCounter[cell.myState] + 1
	
		return stateCounter


	### --- saving the results of the simulation to the .txt file --- ####
	def saveResultToFile(self):
		filename = "resultOfSimulation" + self.numberOfSimulation + ".txt"
		pass

		
	### --- saving the coordinates of initial Infected1 cells to .txt file --- ###
	def saveInitialCoordinatesI1Cells(self):
		filename = "initialCoordinatesCellI1" + self.numberOfSimulation + ".txt"
		pass


	### --- saving the whole simiulation to file: number of iterations, size of World and state of each cell in each iteration --- ###
	def saveWHileSimiulationToFile(self):
		filename = "simulation" + self.numberOfSimulation + ".txt"
		pass