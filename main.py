from classes.World import *
from classes.Cell import *

import sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		cellsNumberInAxis = int(sys.argv[1])
	else:
		cellsNumberInAxis = 10
	if len(sys.argv) > 2:
		numberOfIterations = int(sys.argv[2])
	else:
		numberOfIterations = 20

	
	myWorld = World(rows = cellsNumberInAxis,
					cols = cellsNumberInAxis,
					layers = cellsNumberInAxis,
					numberOfIterations = numberOfIterations,
					numberOfSimulation = 1,
					visualise = True)

	myWorld.simulateWorld()
