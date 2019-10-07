import unittest
from classes.World import *
from classes.Cell import *

class TestWorld_populateCellNeighborhood(unittest.TestCase):

	def getListOfMatesIndexes(self, l, r, c):
		return [		[l-1, r-1, c-1],	[l-1, r-1, c],	[l-1, r-1, c+1],
						[l-1, r,   c-1],	[l-1, r,   c],	[l-1, r,   c+1],
						[l-1, r+1, c-1],	[l-1, r+1, c],	[l-1, r+1, c+1],
						[l,   r-1, c-1],	[l,   r-1, c],	[l,   r-1, c+1],
						[l,   r,   c-1],					[l,   r,   c+1],
						[l,   r+1, c-1],	[l,   r+1, c],	[l,   r+1, c+1],
						[l+1, r-1, c-1],	[l+1, r-1, c],	[l+1, r-1, c+1],
						[l+1, r,   c-1],	[l+1, r,   c],	[l+1, r,   c+1],
						[l+1, r+1, c-1],	[l+1, r+1, c],	[l+1, r+1, c+1]
				]
	
	def worldSetUp(self, cellsNumberInAxis):
		testWorld = World(rows = cellsNumberInAxis,
						cols = cellsNumberInAxis,
						layers = cellsNumberInAxis)

		return testWorld
	
	def test_matesOfMiddleCell(self):
		cellsNumberInAxis = 5
		testWorld = self.worldSetUp(cellsNumberInAxis)
		
		l = 2; r = 2; c = 2
		testingCell = testWorld.cellsList[l][r][c]

		indOfMates = self.getListOfMatesIndexes(l,r,c)

		cellOfAllMates = testingCell.wallMates + testingCell.pointMates + testingCell.lineMates
		counter = 0

		for mate in cellOfAllMates:
			cordinatesMate = [mate.myZ, mate.myX, mate.myY]
			for ind in indOfMates:
				if (cordinatesMate[0] == ind[0]):
					if (cordinatesMate[1] == ind[1]):
						if (cordinatesMate[2] == ind[2]):
							counter = counter + 1
							indOfMates.remove(ind)

		self.assertEqual(counter, 26)

		# cellInd = [0, 0, 0]
		# testingCell = testWorld.cellsList[cellInd[0]][cellInd[1]][cellInd[2]]
		# cellInd = [2, 2, 0]
		# testingCell = testWorld.cellsList[cellInd[0]][cellInd[1]][cellInd[2]]
		

	def test_matesOfNarrowCell(self):
		cellsNumberInAxis = 5
		testWorld = self.worldSetUp(cellsNumberInAxis)
		
		l = 0; r = 0; c = 0
		testingCell = testWorld.cellsList[l][r][c]

		indOfMates = self.getListOfMatesIndexes(l,r,c)

		for ind in indOfMates:
			for i in range(0, len(ind)):
				if (ind[i] >= cellsNumberInAxis):
					ind[i] = 0
				elif (ind[i] == -1):
					ind[i] = cellsNumberInAxis - 1
    				

		cellOfAllMates = testingCell.wallMates + testingCell.pointMates + testingCell.lineMates
		counter = 0

		for mate in cellOfAllMates:
			cordinatesMate = [mate.myZ, mate.myX, mate.myY]
			for ind in indOfMates:
				if (cordinatesMate[0] == ind[0]):
					if (cordinatesMate[1] == ind[1]):
						if (cordinatesMate[2] == ind[2]):
							counter = counter + 1
							indOfMates.remove(ind)
    				
		self.assertEqual(counter, 26)

	def test_matesOfBorderCell(self):
		cellsNumberInAxis = 5
		testWorld = self.worldSetUp(cellsNumberInAxis)
		
		l = 2; r = 2; c = 0
		testingCell = testWorld.cellsList[l][r][c]

		indOfMates = self.getListOfMatesIndexes(l,r,c)

		for ind in indOfMates:
			for i in range(0, len(ind)):
				if (ind[i] >= cellsNumberInAxis):
					ind[i] = 0
				elif (ind[i] == -1):
					ind[i] = cellsNumberInAxis - 1
    	
		cellOfAllMates = testingCell.wallMates + testingCell.pointMates + testingCell.lineMates
		counter = 0

		for mate in cellOfAllMates:
			cordinatesMate = [mate.myZ, mate.myX, mate.myY]
			for ind in indOfMates:
				if (cordinatesMate[0] == ind[0]):
					if (cordinatesMate[1] == ind[1]):
						if (cordinatesMate[2] == ind[2]):
							counter = counter + 1
							indOfMates.remove(ind)
						
		self.assertEqual(counter, 26)

if __name__ == '__main__':
	unittest.main()