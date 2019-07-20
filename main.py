from classes.World import *
from classes.Cell import *
import OpenGL
import pygame

if __name__ == '__main__':
	cellsNumberInAxis = 50
	numberOfIterations = 10
	myWolrd = World(rows = cellsNumberInAxis,
					cols = cellsNumberInAxis,
					layers = cellsNumberInAxis,
					numberOfIterations = numberOfIterations,
					numberOfSimulation = 1)
	# myWolrd.printWorld()
	myWolrd.simulateWorld()

	#comment