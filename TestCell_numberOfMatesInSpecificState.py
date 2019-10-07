import unittest
from classes.Cell import *
from classes.World import *

class TestCell_numberOfMatesInSpecificState(unittest.TestCase):
    
	def setUp(self):
		self.healthy = 0
		self.infected1 = 1
		self.infected2 = 2
		self.dead = 3
		self.cell = Cell()
		self.listOfStates = [self.healthy, self.infected1, self.infected2, self.dead]

	def mySetUp(self, listOfStates, listOfNumberOfCellInEachState):
		listOfCells = []
		for i in range(0, len(listOfStates)):
			tmp = [Cell(myState = listOfStates[i])] * listOfNumberOfCellInEachState[i]
			listOfCells = listOfCells + tmp
		
		return listOfCells
		
	########## -------- FIRST TEST CASES -------- ##########
	def testPart1_numberOfMatesInOneState(self):
		listOfNumberOfCellInEachState = [2, 0, 0, 0]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)
		
		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])

	def testPart1_numberOfMatesInTwoStates(self):
		listOfNumberOfCellInEachState = [2, 3, 0, 0]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)
		
		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])

	def testPart1_numberOfMatesInThreeStates(self):
		listOfNumberOfCellInEachState = [2, 3, 4, 0]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)
		
		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])

	def testPart1_numberOfMatesInFourStates(self):
		listOfNumberOfCellInEachState = [2, 3, 4, 5]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)

		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])


	########## -------- SECOND TEST CASES -------- ##########
	def testPart2_numberOfMatesInOneState(self):
		listOfNumberOfCellInEachState = [8, 0, 0, 0]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)
		
		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])

	def testPart2_numberOfMatesInTwoStates(self):
		listOfNumberOfCellInEachState = [7, 6, 0, 0]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)
		
		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])

	def testPart2_numberOfMatesInThreeStates(self):
		listOfNumberOfCellInEachState = [11, 25, 33, 0]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)
		
		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])

	def testPart2_numberOfMatesInFourStates(self):
		listOfNumberOfCellInEachState = [155, 478, 1125, 44]
		listOfCells = self.mySetUp(self.listOfStates, listOfNumberOfCellInEachState)

		healthyMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.healthy)
		infected1Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected1)
		infected2Mates = self.cell.numberOfMatesInSpecificState(listOfCells, self.infected2)
		deadMates = self.cell.numberOfMatesInSpecificState(listOfCells, self.dead)

		self.assertEqual(healthyMates, listOfNumberOfCellInEachState[0])
		self.assertEqual(infected1Mates, listOfNumberOfCellInEachState[1])
		self.assertEqual(infected2Mates, listOfNumberOfCellInEachState[2])
		self.assertEqual(deadMates, listOfNumberOfCellInEachState[3])


if __name__ == '__main__':
    unittest.main()