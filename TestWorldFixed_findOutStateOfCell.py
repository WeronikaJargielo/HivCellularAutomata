import unittest
from classes.World import *
from classes.Cell import *


### --- description --- ###
# TESTING:
# - fixed boundary codition
# - each rule of changing states by cells
# - grid 5x5x5

class TestWorldFixed_findOutStateOfCell(unittest.TestCase):

	def setUp(self):

		self.healthy = 0
		self.infected1 = 1
		self.infected2 = 2
		self.dead = 3

	def worldSetUp(self, cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV):
		testWorld = World(rows = cellsNumberInAxis,
							cols = cellsNumberInAxis,
							layers = cellsNumberInAxis,
							pHIV = pHIV, 
							boundaryCondition = BoundaryConditions.fixed,
							numberOfIterationsInI1State = numberOfIterationsInI1State,
							numberOfIterationsInI2State = numberOfIterationsInI2State)
		return testWorld

	### --- HEALTHY --> INFECTED 1 --- ###
	### --- coditions for I1 cells --- ###
	def cellSetUp_I1Cell(self, listOfNumberOfCellInNeighborhood, testWorld, zTestingCell, xTestingCell, yTestingCell):
		
		centerCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell]
		centerCell.myState = self.healthy
		wallMatesOfCell = centerCell.wallMates
		lineMatesOfCell = centerCell.lineMates
		pointMatesOfCell = centerCell.pointMates

		numberOfI1CellbyWall = listOfNumberOfCellInNeighborhood[0]
		numberOfI1CellbyLine = listOfNumberOfCellInNeighborhood[1]
		numberOfI1CellbyPoint = listOfNumberOfCellInNeighborhood[2]
		
		for i in range(0, numberOfI1CellbyWall):
			wallMatesOfCell[i].myState = self.infected1

		for i in range(0, numberOfI1CellbyLine):
			lineMatesOfCell[i].myState = self.infected1

		for i in range(0, numberOfI1CellbyPoint):
			pointMatesOfCell[i].myState = self.infected1

		return centerCell


	### --- coditions for I2 cells --- ###
	def cellSetUp_I2Cell(self, listOfNumberOfCellInNeighborhood, testWorld, zTestingCell, xTestingCell, yTestingCell):
		
		centerCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell]
		centerCell.myState = self.healthy
		wallMatesOfCell = centerCell.wallMates
		lineMatesOfCell = centerCell.lineMates
		pointMatesOfCell = centerCell.pointMates
	
		numberOfI2CellbyWall = listOfNumberOfCellInNeighborhood[0]
		numberOfI2CellbyLine = listOfNumberOfCellInNeighborhood[1]
		numberOfI2CellbyPoint = listOfNumberOfCellInNeighborhood[2]

		for i in range(0, numberOfI2CellbyWall):
			wallMatesOfCell[i].myState = self.infected2

		for i in range(0, numberOfI2CellbyLine):
			lineMatesOfCell[i].myState = self.infected2

		for i in range(0, numberOfI2CellbyPoint):
			pointMatesOfCell[i].myState = self.infected2	

		return centerCell


	### --- tests for conditions for I1 cells --- ###
	def testCase1_fromHtoI1byI1Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [1, 0, 0]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I1Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	

			
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.infected1)	
	

	def testCase2_fromHtoI1byI1Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [1, 1, 0]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I1Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	


		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.infected1)	


	def testCase3_fromHtoI1byI1Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [1, 1, 1]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I1Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	
		
			
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.infected1)		
	
	def testCase4_fromHtoI1byI1Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [0, 1, 1]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I1Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	
		
		
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.infected1)	


	def testCase5_fromHtoI1byI1Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [0, 0, 1]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I1Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	
		
		
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.healthy)	

		
	
	def testCase1_fromHtoI1byI2Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [5, 9, 4]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I2Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	

			
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.infected1)	
	

	def testCase2_fromHtoI1byI2Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [4, 9, 4]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I2Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	

			
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.healthy)	


	def testCase3_fromHtoI1byI2Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [5, 9, 2]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I2Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	
		
			
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.healthy)		
	
	def testCase4_fromHtoI1byI2Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [4, 8, 3]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I2Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	
		
		
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.healthy)	


	def testCase5_fromHtoI1byI2Cells(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [6, 11, 7]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		centerCell = self.cellSetUp_I2Cell(listOfNumberOfCellInNeighborhood, testWorld, 
											zTestingCell, xTestingCell, yTestingCell)	
		
			
		testWorld.findOutStateOfCell(centerCell)
		centerCell.myState = centerCell.newState
		stateOfCenterCell = centerCell.myState
		self.assertEqual(stateOfCenterCell, self.infected1)


	# ### --- INFECTED 1 --> INFECTED 2 --- ###

	def testCase1_fromI1toI2(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		testingCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell] # center cell

		testingCell.myState = self.infected1
		testingCell.numberOfI1Iterations = 1
			
		for i in range(0, numberOfIterationsInI1State):	
			testWorld.findOutStateOfCell(testingCell)
			testingCell.myState = testingCell.newState

		stateOfCenterCell = testingCell.myState
		self.assertEqual(stateOfCenterCell, self.infected2)	
	

	def testCase2_fromI1toI2(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		testingCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell] # center cell

		testingCell.myState = self.infected1
		testingCell.newState = self.infected1
		testingCell.numberOfI1Iterations = 1

		for i in range(0, numberOfIterationsInI1State):	
			testWorld.findOutStateOfCell(testingCell)
			testingCell.myState = testingCell.newState

		stateOfCenterCell = testingCell.myState
		self.assertEqual(stateOfCenterCell, self.infected2)

	
	def testCase3_fromI1toI2(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 5; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		testingCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell] # center cell

		testingCell.myState = self.infected1
		testingCell.newState = self.infected1
		testingCell.numberOfI1Iterations = 1

		for i in range(0, numberOfIterationsInI1State):	
			testWorld.findOutStateOfCell(testingCell)
			testingCell.myState = testingCell.newState

		stateOfCenterCell = testingCell.myState
		self.assertEqual(stateOfCenterCell, self.infected2)


	### --- INFECTED --> DEAD --- ###
	def testCase1_fromI2toD(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		testingCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell] # center cell

		testingCell.myState = self.infected2
		testingCell.newState = self.infected2
		testingCell.numberOfI2Iterations = 1

		for i in range(0, numberOfIterationsInI2State):	
			testWorld.findOutStateOfCell(testingCell)
			testingCell.myState = testingCell.newState

		stateOfCenterCell = testingCell.myState
		self.assertEqual(stateOfCenterCell, self.dead)


	def testCase2_fromI2toD(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 3; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		testingCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell] # center cell

		testingCell.myState = self.infected2
		testingCell.newState = self.infected2
		testingCell.numberOfI2Iterations = 1

		for i in range(0, numberOfIterationsInI2State):	
			testWorld.findOutStateOfCell(testingCell)
			testingCell.myState = testingCell.newState

		stateOfCenterCell = testingCell.myState
		self.assertEqual(stateOfCenterCell, self.dead)


	def testCase3_fromI2toD(self):
		cellsNumberInAxis = 5; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 5; pHIV = [0, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		zTestingCell = xTestingCell = yTestingCell = round(cellsNumberInAxis/2)
		testingCell = testWorld.cellsList[zTestingCell][xTestingCell][yTestingCell] # center cell

		testingCell.myState = self.infected2
		testingCell.newState = self.infected2
		testingCell.numberOfI2Iterations = 1

		for i in range(0, numberOfIterationsInI2State):	
			testWorld.findOutStateOfCell(testingCell)
			testingCell.myState = testingCell.newState

		stateOfCenterCell = testingCell.myState
		self.assertEqual(stateOfCenterCell, self.dead)

	### --- CHECKING IF THE BORDER CELLS DO NOT CHANGE --- ###
	def test_borderCellDoNotChangeState(self):
		cellsNumberInAxis = 3; numberOfIterationsInI1State = 1; numberOfIterationsInI2State = 2; pHIV = [1, 1]
		testWorld = self.worldSetUp(cellsNumberInAxis, numberOfIterationsInI1State, numberOfIterationsInI2State, pHIV)

		listOfNumberOfCellInNeighborhood = [1,1,1]; testWorld = testWorld
		zTestingCell = xTestingCell = yTestingCell = 0
		testingCell = self.cellSetUp_I1Cell(listOfNumberOfCellInNeighborhood, testWorld, 
										zTestingCell, xTestingCell, yTestingCell)

		testWorld.findOutStateOfCell(testingCell)
		testingCell.myState = testingCell.newState
		self.assertEqual(testingCell.myState, self.healthy)

if __name__ == '__main__':
    unittest.main()


