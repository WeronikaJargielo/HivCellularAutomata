from classes.Cell import *
from classes.Probability import *
from classes.Visualisation import *
from classes.BoundaryConditions import *
import random
from time import sleep, time
from _thread import start_new_thread
from threading import Semaphore, Thread
from os import path # library to operate on files
from sys import exit

import multiprocessing
from joblib import Parallel, delayed

class World:
	### --- constructor of class World --- ###
	def __init__(self,**kwargs):

		### --- simulation parameters --- ###
		self.rows = kwargs.get('rows', 100) 
		self.cols = kwargs.get('cols', 100)
		self.layers = kwargs.get('layers', 100)

		self.numberOfCells = self.rows * self.cols * self.layers
		self.numberOfIterations = kwargs.get('numberOfIterations', 30)
		
		self.visualisation_ON = kwargs.get('visualisation_ON', False)
		self.saveSimulation_ON = kwargs.get('saveSimulation_ON', False)

		self.nameOfFile = kwargs.get('nameOfFile', str(random.randint(0,100)))
		self.nameOfDirForResults = 'results_of_simulation'
		
		### --- states --- ###
		self.healthy = 0
		self.infected1 = 1
		self.infected2 = 2
		self.dead = 3

		### --- Initial conditions --- ###
		# the percentage (probability) of initial healthy cell infected by HIV 
		# self.pInitialHIV = kwargs.get('pInitialHIV', 0.0005) # from Alive to I1
		self.pHIV = kwargs.get('pHIV', [5, 10000]) # from Alive to I1
		self.pInitialHIV = Probability(nominator = self.pHIV[0], denominator = self.pHIV[1])

		### --- boundary conditions --- ###
		self.boundaryCondition = kwargs.get('boundaryCondition', BoundaryConditions.fixed)

		### --- RULES --- ###

		# RULES 1 FOR: Healthy Cell --> Infected 1 Cell
		self.numI1Cell_WallMates = kwargs.get('numI1Cell_WallMates', 1)  
		self.numI1Cell_LineMates = kwargs.get('numI1Cell_LineMates', 1)

		self.numI2Cell_WallMates = kwargs.get('numI2Cell_WallMates', 5) 
		self.numI2Cell_LineMates = kwargs.get('numI2Cell_LineMates', 9)
		self.numI2Cell_PointMates = kwargs.get('numI2Cell_PointMates', 4)

		# RULES 2 FOR: Infected 1 Cell --> Infected 2 Cell - after particular number of iterations in state I1
		self.numberOfIterationsInI1State = kwargs.get('numberOfIterationsInI1State', 1)

		# RULES 3 FOR: Infected 2 Cell --> Dead Cell - after particular number of iterations in state I2
		self.numberOfIterationsInI2State = kwargs.get('numberOfIterationsInI2State', 2)
		
		# RULES 4 FOR: 
		# 				Dead Cell --> Infected 1 Cell: with propability of infection - pInf
		# 				Dead Cell --> Healthy Cell: with propability of replenision - pRep

		# probability that DEAD cell is replenished by HEALTHY cell 
		self.pRep = kwargs.get('pRep', [99, 100])
		self.pReplenision = Probability(nominator = self.pRep[0], denominator = self.pRep[1])

		# probability that DEAD cell becomes INFECTED 1 cell
		self.pInf = kwargs.get('pInf', [974, 100000000])
		self.pInfection = Probability(nominator = self.pInf[0] , denominator = self.pInf[1]) 

		# make common denominator
		self.pInfection.commonDenominator(self.pReplenision)

		self.createDirForResultFiles()

		self.cellsListToDisplay = [[],[],[]]	# list of list of cells in specific state that should be displayed in this iteration
												# [0] - Infected1
												# [1] - Infected2
												# [2] - Dead

		self.cellsList = []
		self.createWorld()
		self.setStateOfInitialI1Cells()
		self.setAllCellsMates()
		
		self.createSemaphoresForVisualisation()

	### --- creation of the world --- ###
	def createWorld(self):
		for l in range(self.layers):
			singleLayer = []
			for r in range(self.rows):
				singleRow = []
				for c in range(self.cols):
					cell = Cell(myX = r, myY = c, myZ = l)
					singleRow.append(cell)
					cell.setIsBorderCell(self.layers, self.rows, self.cols)

				singleLayer.append(singleRow)
			self.cellsList.append(singleLayer)


	### --- setting initially infected 1 cells --- ###
	def setStateOfInitialI1Cells(self): 
		for layer in self.cellsList:
			for row in layer:
				for cell in row:
					if ((self.boundaryCondition == BoundaryConditions.periodic) or (cell.isBorderCell == False)):
						randomProbability = random.randrange(0, self.pInitialHIV.denominator)
						if randomProbability < self.pInitialHIV.nominator: 
							cell.myState = self.infected1
							cell.newState = self.infected1
							
							if self.visualisation_ON:
								self.cellsListToDisplay[cell.myState - 1].append(cell)

	### --- creates semaphores for synchronizing simulation and visualisation --- ###
	def createSemaphoresForVisualisation(self):
		if self.visualisation_ON:
			self.displaySemaphore = Semaphore()
			self.simulationSemaphore = Semaphore()


	### --- finds out the state of particular cell --- ###
	def findOutStateOfCell(self, cell):
    		
		# HEALTHY --> INFECTED 1
		if cell.myState == self.healthy:
			self.checkIfHealthyBecomesI1(cell)	

		# INFECTED 1 --> INFECTED 2
		elif cell.myState == self.infected1: 
			self.checkIfI1BecomesI2(cell)	

		# INFECTED 2 --> DEAD
		elif cell.myState == self.infected2:
			self.checkIfI2BecomesDead(cell)

		# FROM DEAD
		elif cell.myState == self.dead:
			self.checkIfDeadBecomesI1OrHealthy(cell)

		else:
			print('Unknown state')
			exit()

	### --- HEALTHY --> INFECTED 1 --- ###
	def checkIfHealthyBecomesI1(self, cell):
		if 	((self.boundaryCondition == BoundaryConditions.periodic) or (cell.isBorderCell == False)):	
			if (	cell.numberOfMatesInSpecificState(cell.wallMates, self.infected1) >= self.numI1Cell_WallMates # I1 cell, wall neighborhood
					or cell.numberOfMatesInSpecificState(cell.lineMates, self.infected1) >= self.numI1Cell_LineMates # I1 cell, line neighborhood
					or (
						cell.numberOfMatesInSpecificState(cell.wallMates, self.infected2) >= self.numI2Cell_WallMates # I2 cell, wall neighborhood
					and cell.numberOfMatesInSpecificState(cell.lineMates, self.infected2) >= self.numI2Cell_LineMates # I2 cell, line neighborhood
					and cell.numberOfMatesInSpecificState(cell.pointMates, self.infected2) >= self.numI2Cell_PointMates # I2 cell, point neighborhood
					)
				):
				cell.newState = self.infected1
				cell.numberOfI1Iterations = 1
		

	### --- INFECTED 1 --> INFECTED 2 --- ###
	def checkIfI1BecomesI2(self, cell):	
		if cell.numberOfI1Iterations >= self.numberOfIterationsInI1State:
			cell.newState = self.infected2
			cell.numberOfI2Iterations = 1
		else:
			cell.numberOfI1Iterations = cell.numberOfI1Iterations + 1


	### --- INFECTED 2 --> DEAD --- ###
	def checkIfI2BecomesDead(self, cell):
		if cell.numberOfI2Iterations >= self.numberOfIterationsInI2State:
			cell.newState = self.dead
		else:
			cell.numberOfI2Iterations = cell.numberOfI2Iterations + 1
		

	### --- DEAD --> INFECTED 1/HEALTHY --- ###
	def checkIfDeadBecomesI1OrHealthy(self, cell):
		randomProbability = random.randrange(0, self.pInfection.denominator)
			
		# DEAD --> INFECTED 1
		if randomProbability < self.pInfection.nominator:
			cell.newState = self.infected1

		# DEAD --> HEALTHY
		elif randomProbability < self.pReplenision.nominator: # (Prep-Pinf) remaining probability 
			cell.newState = self.healthy


	### --- setting cell's neighbours --- ###
	def setAllCellsMates(self):
		for layer in self.cellsList:
			for row in layer:
				for cell in row:
					self.populateCellNeighborhood(cell)


	### --- fills cell's neighborhoods --- ###
	def populateCellNeighborhood(self, cell):
		l = cell.myZ
		r = cell.myX
		c = cell.myY

		lRange = list(range(l-1, l+2))  # create range [first, last)
		rRange = list(range(r-1, r+2))
		cRange = list(range(c-1, c+2))

		if l+1 == self.layers: # checking if value is not out of range
			lRange[2] = 0   
		if r+1 == self.rows:
			rRange[2] = 0  
		if c+1 == self.cols:
			cRange[2] = 0  

		for ll in lRange:
			for rr in rRange:
				for cc in cRange:
					neighborCell = self.cellsList[ll][rr][cc] 
					self.addNeighborToNeighborhoodOfCell(cell, neighborCell)
							
	
	### --- adds neighbor to specific kind of neighborhood of the cells --- ###
	def addNeighborToNeighborhoodOfCell(self, cell, neighborCell):
		# number of different indices for specific neighbors:
		wallNeighbors = 1				
		lineNeighbors = 2
		pointNeighbors = 3
		
		differentIndexes = (neighborCell.myZ != cell.myZ) + (neighborCell.myX != cell.myX) + (neighborCell.myY != cell.myY)
		if differentIndexes == pointNeighbors:
			cell.pointMates.append(neighborCell)
		elif differentIndexes == lineNeighbors:
			cell.lineMates.append(neighborCell)
		elif differentIndexes == wallNeighbors:
			cell.wallMates.append(neighborCell)


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
		
	### --- performs simulation of whole world --- ###
	def calculateWholeSimulation(self, visualisation):
		sleep(1)	# wait for display initialization

		for i in range(self.numberOfIterations):
			self.singleIteration(visualisation, i)


	### --- performs single iteration of simulation --- ###
	def singleIteration(self, visualisation, iterationNumber):
		if self.saveSimulation_ON:
			self.saveResultToFile(iterationNumber, self.countCellsInSpecificState())

		if self.visualisation_ON:
			self.simulationSemaphore.acquire()

		try:
			loopTime = time()
			
			self.findOutAllCellsStates()

			self.updateAllCellsStates()

			loopTime = time() - loopTime
			print(iterationNumber, " loop time: ", loopTime)
			
			if self.visualisation_ON:
				visualisation.refreshDisplay(self.cellsListToDisplay)
		
		finally:
			if self.visualisation_ON:
				self.displaySemaphore.release()

	### --- finds out new state of all cells --- ###
	def findOutAllCellsStates(self):
		for layer in self.cellsList:
			for row in layer:
				for cell in row:
					self.findOutStateOfCell(cell)


	### --- updating all cell's states at the same time --- ###
	def updateAllCellsStates(self):
		if self.visualisation_ON:
			self.cellsListToDisplay = [[], [], []]
		
		for layer in self.cellsList:
			for row in layer:
				for cell in row:
					cell.myState = cell.newState
					
					if self.visualisation_ON and cell.myState:			# dont draw healthy cells
						self.cellsListToDisplay[cell.myState - 1].append(cell)


	### --- counting the cells in particular state on the grid --- ###
	def countCellsInSpecificState(self):
		stateCounter = [0, 0, 0, 0] # H, I1, I2, D
		for layer in self.cellsList:
			for row in layer:
				for cell in row:
					stateCounter[cell.myState] =  stateCounter[cell.myState] + 1
		return stateCounter

	### --- creats directory for the results --- ###
	def createDirForResultFiles(self):
		if (self.saveSimulation_ON):
			if (not path.isdir(self.nameOfDirForResults)):
				os.mkdir(self.nameOfDirForResults)
			self.initializeFileToSaveResult()

	### --- saves the results of sigle iteration of the simulation to the .txt file --- ####
	def saveResultToFile(self, iteration, listOfCountedCellEachState):
		filename = self.nameOfDirForResults + '/' + self.nameOfFile + '.txt'
		file = open(filename, "a") # opening the file in append mode to save simulation
		file.write('\n' + str(iteration) + '\t')
		for state in listOfCountedCellEachState:
			file.write(str(state) + '\t')
		file.close()


	### --- initializes .txt file for saving results of simulation--- ####
	def initializeFileToSaveResult(self):
		filename = self.nameOfDirForResults + '/' + self.nameOfFile + '.txt'
		file = open(filename, "w") # opening the file to save simulation
		colNames = ['%Iteration','Healthy', 'Infected_1', 'Infected_2', 'Dead']
		description = ['%pHIV = ', str(self.pHIV), '; pINF = ', str(self.pInf),
						'; I1Iterations = ', str(self.numberOfIterationsInI1State),
						'; I2Iterations = ', str(self.numberOfIterationsInI2State),
						'; boundaryCodition = ', str(self.boundaryCondition.name)]
		print(description)
		lists = [description, colNames]
	
		for l in lists:
			for name in l:
				file.write(name)
			file.write('\n')
		file.close()
 