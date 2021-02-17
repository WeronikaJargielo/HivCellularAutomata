from classes.BoundaryConditions import BoundaryConditions
from classes.World import World

import sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		cellsNumberInAxis = int(sys.argv[1])
	else:
		cellsNumberInAxis = 30
	if len(sys.argv) > 2:
		numberOfIterations = int(sys.argv[2])
	else:
		numberOfIterations = 20
	if len(sys.argv) > 3:
		nameOfFileSim = str(sys.argv[3])
	else:
		nameOfFile = 'noNameFile'
	

	### --- run many simulation for each set of conditions --- ###
	# numberOfIterations = 50
	# cellsNumberInAxis = 20
	# numberOfIterations = 5
	# cellsNumberInAxis = 5
	
	# all available parameters
	pINF = [[1, 100000], [1, 10000], [974, 100*1000000], [974, 100*100000],[974, 100*10000]]
	pHIV = [[5, 100], [5, 1000], [5, 10000]]
	tau = [2,3,4,5]
	boundaryConditions = [BoundaryConditions.fixed, BoundaryConditions.periodic]
	
	numberOfRepetitions = [0, 1]

	# 	boundaryCondition				I1->I2		I2->Dead	pINF					pHIV		
	parameters = [
		# [BoundaryConditions.fixed, 		1,			2,			[1, 10000],				[5, 10000]	],
		# [BoundaryConditions.fixed, 		1,			2,			[5, 100000],			[5, 1000]	],
		# [BoundaryConditions.fixed, 		1,			2,			[974, 100*100000],		[5, 10000]	],
		# [BoundaryConditions.fixed, 		1,			2,			[1, 100000],			[5, 1000]	],
		# [BoundaryConditions.fixed, 		1,			2,			[1, 100000],			[5, 10000]	],
		# [BoundaryConditions.fixed, 		1,			2,			[1, 10000],				[5, 1000]	],
		# [BoundaryConditions.fixed, 		1,			3,			[1, 10000],				[5, 1000]	],
		# [BoundaryConditions.fixed, 		1,			4,			[1, 10000],				[5, 1000]	],
		# [BoundaryConditions.fixed, 		1,			2,			[974, 100*1000000],		[5, 1000]	],
		# [BoundaryConditions.fixed, 		1,			2,			[974, 100*1000000],		[5, 100]	],
		# [BoundaryConditions.fixed, 		1,			2,			[974, 100*1000000],		[5, 10000]	]
		# [BoundaryConditions.fixed, 		1,			2,			[974, 100*100000],		[5, 1000]	],

		# [BoundaryConditions.periodic, 	1,			2,			[1, 100000],			[5, 10000]	],
		# [BoundaryConditions.periodic, 	1,			2,			[1, 10000],				[5, 10000]	],
		[BoundaryConditions.periodic, 	1,			2,			[1, 10000],				[5, 1000]	],

		# [BoundaryConditions.periodic, 	1,			2,			[974, 100*1000000],		[5, 1000]	],
		
		# [BoundaryConditions.periodic, 	1,			2,			[974, 100*100000],		[5, 10000]	],
		# [BoundaryConditions.periodic, 	1,			4,			[974, 100*100000],		[5, 10000]	],
		# [BoundaryConditions.periodic, 	1,			2,			[974, 100*100000],		[5, 1000]	],
	]

	for rep in range(numberOfRepetitions[0], numberOfRepetitions[1]):
		for [bc, i1ToI2, i2ToDead, pInf, pHiv] in parameters:
			nameOfFile = str(bc.name) + '_' + str(i1ToI2) + '_' + str(i2ToDead) + '_' + str(pInf) + '_' + str(pHiv) + '_' + str(rep)
			myWorld = World(rows = cellsNumberInAxis,
						cols = cellsNumberInAxis,
						layers = cellsNumberInAxis,
						numberOfIterations = numberOfIterations,
						numberOfIterationsInI1State = i1ToI2,
						numberOfIterationsInI2State = i2ToDead,
						pInf = pInf,
						pHIV = pHiv,
						boundaryCondition = bc,
						visualisation_ON = True,
						saveSimulation_ON = False,
						nameOfFile = nameOfFile)

			myWorld.simulateWorld()
	