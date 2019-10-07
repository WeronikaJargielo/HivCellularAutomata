from classes.World import *
from classes.Cell import *
from classes.BoundaryConditions import *

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
	if len(sys.argv) > 3:
    		nameOfFile = str(sys.argv[3])
	else:
		nameOfFile = 'noNameFile'


	# ### --- single simulation --- ###
	# myWorld = World(rows = cellsNumberInAxis,
	# 				cols = cellsNumberInAxis,
	# 				layers = cellsNumberInAxis,
	# 				numberOfIterations = numberOfIterations,
	# 				pInf = [1, 100000],
	# 				pHIV = [5, 100],
	# 				boundaryCondition = BoundaryConditions.periodic,
	# 				numberOfIterationsInI1State = 2,
	# 				numberOfIterationsInI2State = 2,
	# 				visualisation_ON = True,
	# 				saveSimulation_ON = False,
	# 				nameOfFile = nameOfFile)

	# myWorld.simulateWorld()


	### --- testing periodic boudary condition--- ###
	numberOfIterations = 1050
	cellsNumberInAxis = 100
	
	pHIV = [[5, 100], [5, 1000], [5, 10000]]
	pINF = [[1, 100000], [1, 10000], [974, 100*1000000], [974, 100*100000],[974, 100*10000]]
	tau = [2,3,4,5]
	boundaryConditions = [BoundaryConditions.fixed, BoundaryConditions.periodic]
	
	for bc in boundaryConditions:
		for i in pINF:
			for j in pHIV:
				for k in tau:
					nameOfFile = str(bc.name) + '_' + str(i) + '_' + str(j) + '_' + str(k)
					myWorld = World(rows = cellsNumberInAxis,
								cols = cellsNumberInAxis,
								layers = cellsNumberInAxis,
								numberOfIterations = numberOfIterations,
								numberOfIterationsInI1State = k,
								# numberOfIterationsInI2State = k,
								pInf = i,
								pHIV = j,
								boundaryCondition = bc,
								visualisation_ON = False,
								saveSimulation_ON = True,
								nameOfFile = nameOfFile)

					myWorld.simulateWorld()


	### --- repeating simulation --- ###
	# for i in range(8):
	# 	nameOfFile = 'foolHope' + str(i)
	# 	myWorld = World(rows = cellsNumberInAxis,
	# 					cols = cellsNumberInAxis,
	# 					layers = cellsNumberInAxis,
	# 					numberOfIterations = numberOfIterations,
	# 					# pInf = [1, 100000],
	# 					# pInf = [974, 100000000],
	# 					# pHIV = [5, 100],
	# 					pInf = [500, 100000000],
	# 					visualisation_ON = False,
	# 					saveSimulation_ON = True,
	# 					nameOfFile = nameOfFile)

	# 	myWorld.simulateWorld()

# pInitialHIV = 0.05,
# pRep = [99, 100],
# pInf = [1, 100000],