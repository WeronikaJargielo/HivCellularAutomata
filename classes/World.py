from classes.Cell import *
from classes.Probability import *
from classes.Visualisation import *
import random
from time import sleep, time
from _thread import start_new_thread
from threading import Semaphore, Thread
from os import path # library to operate on files

class World:
	### --- constructor of class World --- ###
	# kwargs.get('nameOfParametr', defaultValue)
	def __init__(self,**kwargs):

		### --- simulation parametrs --- ###
		self.rows = kwargs.get('rows', 100) # numbers of rows - x
		self.cols = kwargs.get('cols', 100) # numbers of cols - y
		self.layers = kwargs.get('layers', 100) # numbers of layers - z
		self.numberOfSimulation = kwargs.get('numberOfSimiulation', -1) # needed in filename during saving to file
		self.dimension = self.rows * self.cols * self.layers # dimension of whole grid
		self.numberOfIterations = kwargs.get('numberOfIterations', 30) # numbers of iterations of simulation
		

		self.visualisation_ON = kwargs.get('visualisation_ON', False) # if visualisation should be displayed
		self.saveSimulation_ON = kwargs.get('saveSimulation_ON', False) # if simulation should be save to TXT file
		self.nameOfFile = kwargs.get('nameOfFile', str(random.randint(0,100))) # name of output file
		self.nameOfDictForResults = 'results_Of_Simulation' # name of dictionary where will be stored result of simulation

		### --- creating dictionaries for the results --- ###
		if (self.saveSimulation_ON):
			if (not path.isdir(self.nameOfDictForResults)):
				os.mkdir(self.nameOfDictForResults)
			self.initializeFileToSaveResult(self.nameOfFile)	
		
		### --- states --- ###
		self.healthy = 0
		self.infected1 = 1
		self.infected2 = 2
		self.dead = 3

		### --- Initial coditions --- ###
		# the probability/percentage of initial healthy cell infected by HIV 
		self.pInitialHIV = kwargs.get('pInitialHIV', 0.0005) # from Alive to I1

		# initial number of cells of type infected 1
		self.numberOfI1Cell = kwargs.get('numberOfInfected_1_Cell', (self.dimension * self.pInitialHIV)) 
		
		### --- rules --- ###

		# RULES 1 FOR: Healthy Cell --> Infected 1 Cell
		self.numI1Cell_WallMates = kwargs.get('numI1Cell_WallMates', 1)  
		self.numI1Cell_LineMates = kwargs.get('numI1Cell_LineMates', 1)

		self.numI2Cell_WallMates = kwargs.get('numI2Cell_WallMates', 5) 
		self.numI2Cell_LineMates = kwargs.get('numI2Cell_LineMates', 9)
		self.numI2Cell_PointMates = kwargs.get('numI2Cell_PointMates', 4)

		# RULES 2 FOR: Infected 1 Cell --> Infected 2 Cell - in the next step interation

		# RULES 3 FOR: Infected 2 Cell --> Dead Cell - after particular numbers of interation in state I2
		self.numberOfIterationsInI2State = kwargs.get('numberOfIterationsInI2State', 2)
		
		# RULES 4 FOR: 
		# 				Dead Cell --> Infected 1 Cell with propability of infection - P_inf
		# 				Dead Cell --> Healthy Cell with propability of replenision - P_rep

		# probability that a DEAD cell is replenished by an HEALTHY cell 
		self.pRep = kwargs.get('pRep', [99, 100])
		self.pReplenision = Probability(nominator = self.pRep[0], denominator = self.pRep[1])

		
		# probability that a DEAD cell becomes a HEALTHY cell
		self.pInf = kwargs.get('pInf', [974, 100000000])
		self.pInfection = Probability(nominator = self.pInf[0] , denominator = self.pInf[1]) 

		# make common denominator
		self.pInfection.commonDenominator(self.pReplenision)
   
		self.cellsList = [] 
		self.createWorld() # creation of 3D grid of cells
		self.setStateOfIntialI1Cell(self.numberOfI1Cell) # setting the state of I1 cells randomly selected
		self.setCellsMates() # setting neighbours of each cell

		if self.visualisation_ON:
			self.displaySemaphore = Semaphore()
			self.simulationSemaphore = Semaphore()
		
		self.cellsListToDisplay = []	# list of list of cells is specific state that should be displayed in this iteration
										# [0] - Infected1
										# [1] - Infected2
										# [2] - Dead

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
			
			if (	cell.matesInSpecificState(cell.wallMates, self.infected1) >= self.numI1Cell_WallMates # I1 cell, wall neighborhood
				 or cell.matesInSpecificState(cell.lineMates, self.infected1) >= self.numI1Cell_LineMates # I1 cell, line neighborhood
				 or (
						cell.matesInSpecificState(cell.wallMates, self.infected2) >= self.numI2Cell_WallMates # I2 cell, wall neighborhood
					and cell.matesInSpecificState(cell.lineMates, self.infected2) >= self.numI2Cell_LineMates # I2 cell, line neighborhood
					and cell.matesInSpecificState(cell.pointMates, self.infected2) >= self.numI2Cell_PointMates # I2 cell, point neighborhood
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

		wallNeighbors = 1			# number of different indices for specific neighbours
		lineNeighbors = 2
		pointNeighbors = 3

		xMax = self.rows - 1		# max cells indices
		yMax = self.cols - 1
		zMax = self.layers - 1

		for l in range(self.layers):
			for r in range(self.rows):
				for c in range(self.cols):
					cell = self.cellsList[l][r][c] # middle cell

					cell.isBorderCell = cell.checkIfBorder(xMax, yMax, zMax)

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
								differentIndexes = (ll != cell.myZ) + (rr != cell.myX) + (cc != cell.myY)
								if differentIndexes == pointNeighbors:
									cell.pointMates.append(neighbourCell)
								elif differentIndexes == lineNeighbors:
									cell.lineMates.append(neighbourCell)
								elif differentIndexes == wallNeighbors:
									cell.wallMates.append(neighbourCell)

	### --- simulation of world --- ###
	def simulateWorld(self):
		if self.visualisation_ON:
			visualisation = Visualisation(displaySemaphore = self.displaySemaphore,
										simulationSemaphore = self.simulationSemaphore,
										cellsList = self.cellsList,
										cellsListToDisplay = self.cellsListToDisplay
									)
			try:
				thread = Thread(target = self.calculateWholeSimulation, args = (visualisation, ))
				thread.start()
			except:
				print("Unable to start thread")

			visualisation.startDisplayingWorld()
		else:
			self.calculateWholeSimulation(None)
		

	def calculateWholeSimulation(self, visualisation):
		sleep(1)	# wait for display initialization

		for i in range(self.numberOfIterations):
			if self.saveSimulation_ON:
				self.saveResultToFile(self.nameOfFile, i, self.countCellsInSpecificState())

			if self.visualisation_ON:
				self.simulationSemaphore.acquire()

			try:
				loopTime = time()
				
				if self.visualisation_ON:
					self.cellsListToDisplay = [[], [], []]

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
							# if cell.stateChanged:
							cell.myState = cell.newState # update cell.state of cell
							
							if self.visualisation_ON and cell.myState:			# dont draw healthy cells
								self.cellsListToDisplay[cell.myState - 1].append(cell)

				loopTime = time() - loopTime
				print(i, " loop time: ", loopTime)
				
				if self.visualisation_ON:
					visualisation.refreshDisplay(self.cellsListToDisplay)
			
			finally:
				if self.visualisation_ON:
					self.displaySemaphore.release()


	### --- counting the cells in particular state on the grid --- ###
	def countCellsInSpecificState(self):
		stateCounter = [0, 0, 0, 0] # H, I1, I2, D
		for l in range(self.layers):
			for r in range(self.rows):
				for c in range(self.cols):
					cell = self.cellsList[l][r][c]
					stateCounter[cell.myState] =  stateCounter[cell.myState] + 1
	
		return stateCounter


	### --- saving the results of sigle iteration of the simulation to the .txt file --- ####
	def saveResultToFile(self, nameOfFile, iteration, listOfCountedCellEachState):
		filename = self.nameOfDictForResults + '/' + nameOfFile + '.txt'
		file = open(filename, "a") # opening the file to save simulation
		file.write('\n' + str(iteration) + '\t')
		for state in listOfCountedCellEachState:
			file.write(str(state) + '\t')
		file.close()


	### --- initializing .txt file for saving results of simiulation--- ####
	def initializeFileToSaveResult(self, nameOfFile):
		filename = self.nameOfDictForResults + '/' + nameOfFile + '.txt'
		file = open(filename, "a") # opening the file to save simulation
		colNames = ['Iteration','Healthy', 'Infected_1', 'Infected_2', 'Dead']
		for name in colNames:
			file.write(name+'\t')
		file.close()
