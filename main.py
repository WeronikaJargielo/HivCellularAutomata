from classes.World import *
from classes.Cell import *

if __name__ == '__main__':
	cellsNumberInAxis = 100
	numberOfIterations = 1
	myWolrd = World(rows = cellsNumberInAxis,
					cols = cellsNumberInAxis,
					layers = cellsNumberInAxis,
					numberOfIterations = numberOfIterations,
					numberOfSimulation = 1)
	# myWolrd.printWorld()
	myWolrd.simulateWorld()

	#comment