from classes.World import *
from classes.Cell import *

if __name__ == '__main__':
	cellsNumberInAxis = 10
	numberOfIterations = 10
	myWolrd = World(rows = cellsNumberInAxis,
					cols = cellsNumberInAxis,
					layers = cellsNumberInAxis,
					numberOfIterations = numberOfIterations,
					numberOfSimulation = 1,
					visualisation_ON = False,
					saveSimulation_ON = False,
					nameOfFile = 'nope')
	# myWolrd.printWorld()
	# myWolrd.simulateWorld()
	myWolrd.performSimulation()
	
