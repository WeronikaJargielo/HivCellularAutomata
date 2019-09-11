from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

from time import sleep, time
from threading import Semaphore

import random
from array import array

from numpy import array as numpyArray
from numpy import int32

class Visualisation():

	def __init__(self,**kwargs):

		self.windowWidth = kwargs.get('windowWidth', 800)	# main window's width
		self.windowHeight = kwargs.get('windowHeight',600)	# main window's height

		self.cellsList = kwargs.get('cellsList', None)					# list of all cells
		self.cellsInAxis = len(self.cellsList)							# number of little cubes in row
		self.lenBigCube = kwargs.get('bigCubeLength', 3)				# length of frame cube
		self.lenSmallCube = self.lenBigCube / self.cellsInAxis			# length of small cubes

		self.cellsListToDisplay = kwargs.get('cellsListToDisplay', None)	# reference to cells to display
		self.cellsListToDisplay2 = kwargs.get('cellsListToDisplay2', None)	# reference to cells to display divided to one list per state

		# self.timeDelay = kwargs.get('simTimeDelay', 500)

		self.simSem = kwargs.get('simSem', None)
		self.displaySem = kwargs.get('displaySem', None)

		self.vertexesPerCube = 24 # number of vertexes needed for drawing one cube

		self.xCoefficient = 4 * self.vertexesPerCube * self.cellsInAxis * self.cellsInAxis	# coefficients needed to find proper vertex position in VBO in bytes
		self.yCoefficient = 4 * self.vertexesPerCube * self.cellsInAxis
		self.zCoefficient = 4 * self.vertexesPerCube

		self.xCoefficient2 = 8 * self.cellsInAxis * self.cellsInAxis	# coefficients needed to find proper vertex position in VBO
		self.yCoefficient2 = 8 * self.cellsInAxis
		self.zCoefficient2 = 8 

		self.vboId = 0

		self.translateOnX = -self.lenBigCube/4
		self.translateOnY = -self.lenBigCube/2
		self.translateOnZ = -2.5 * self.lenBigCube

# single colors
		self.colBigCube = (255, 255, 255, 255)	# frame cube color - white, opaque
		self.colHealthy = (0, 0, 0, 0)			# healthy cells' color - black, transparent
		self.colInfected1 = (255, 255, 0, 255) 	# infected 1 cells' color - yellow, opaque
		self.colInfected2 = (255, 155, 0, 255) 	# infected 2 cells' color - orange, opaque
		self.colDead = (255, 0, 0, 255) 		# dead cells' color - red, opaque
		self.colList = [self.colHealthy, self.colInfected1, self.colInfected2, self.colDead] # enables setColor(self.colList[cell.state])

# array colors
		self.colAHeal = array('f', [ 0, 0, 0,  	0, 0, 0,  	0, 0, 0,  	  0, 0, 0,  	0, 0, 0,  	0, 0, 0,  	0, 0, 0,  		0, 0, 0]).tostring()	# arrays with cube colors
		self.colAInf1 = array('f', [ 1, 1, 0,  	1, 1, 0,  	0.9, 0.9, 0,  0.8, 0.8, 0,  1, 1, 0,  	1, 1, 0,  	0.95, 0.95, 0,  1, 1, 0]).tostring()
		self.colAInf2 = array('f', [ 1, 0.6, 0, 1, 0.6, 0,  0.9, 0.5, 0,  0.8, 0.4, 0,  1, 0.6, 0,  1, 0.6, 0,  0.95, 0.55, 0,  1, 0.6, 0]).tostring()
		self.colADead = array('f', [ 1, 0, 0,  	1, 0, 0,  	0.9, 0, 0,    0.8, 0, 0,  	1, 0, 0,  	1, 0, 0,  	0.95, 0, 0,  	1, 0, 0] ).tostring()
		self.colAList = [self.colAHeal, self.colAInf1, self.colAInf2, self.colADead] # enables setColor(self.colAList[cell.state])

# array vertices
		self.cubesAVertices = []

		self.surfacesA = array('B', [						# vertices numbers for all surfaces 
				0,1,2,3,	# back wall
				3,2,7,6,	# left wall
				6,7,5,4,	# front wall
				4,5,1,0,	# right wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			]).tostring()
		self.surfacesFrontLeftA = array('B', [						# vertices numbers for top, front and left surfaces 
				6,7,5,4,	# front wall
				3,2,7,6,	# left wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			]).tostring()
		self.surfacesFrontRightA = array('B', [						# vertices numbers for top, front and right surfaces 
				6,7,5,4,	# front wall
				4,5,1,0,	# right wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			]).tostring()
		self.surfacesBackRightA = array('B', [						# vertices numbers for top, back and right surfaces 
				0,1,2,3,	# back wall
				4,5,1,0,	# right wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			]).tostring()
		self.surfacesBackLeftA = array('B', [						# vertices numbers for top, back and left surfaces 
				0,1,2,3,	# back wall				
				3,2,7,6,	# left wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			]).tostring()
		self.currentSurfacesA = None								# array of vertex indices to be displayed in current iteration

# long data
		self.edges = [							# edges for all cubes
					[0,1], [0,3], [0,4], [2,1],
					[2,3], [2,7], [6,3], [6,4],
					[6,7], [5,1], [5,4], [5,7]
					]
		self.verticesBigCube = [				# big cube vertices
				[self.lenBigCube, 	0, 					0],
				[self.lenBigCube, 	self.lenBigCube, 	0],
				[0, 				self.lenBigCube, 	0],
				[0, 				0, 					0],
				[self.lenBigCube, 	0, 					self.lenBigCube],
				[self.lenBigCube, 	self.lenBigCube, 	self.lenBigCube],
				[0, 				0, 					self.lenBigCube],
				[0, 				self.lenBigCube, 	self.lenBigCube]
			]
		self.verticesSmallCube = [				# small cubes vertices
				[self.lenSmallCube, 0, 					0],
				[self.lenSmallCube, self.lenSmallCube, 	0],
				[0, 				self.lenSmallCube, 	0],
				[0, 				0, 					0],
				[self.lenSmallCube, 0, 					self.lenSmallCube],
				[self.lenSmallCube, self.lenSmallCube, 	self.lenSmallCube],
				[0, 				0, 					self.lenSmallCube],
				[0, 				self.lenSmallCube, 	self.lenSmallCube]
			]
		self.cubesVertices = []					# all cubes' vertices
		self.surfaces = [						# vertices numbers for all surfaces 
				[0,1,2,3],	# back wall
				[3,2,7,6],	# left wall
				[6,7,5,4],	# front wall
				[4,5,1,0],	# right wall
				[1,5,7,2],	# top wall
				[4,0,3,6]	# bottom wall
			]
		self.wallMatesIndexes = [				# indexes of cell.wallMates mapped to corresponding surfaces - cell coordinates: x, y, z
				0,	# back wall mate
				2,	# left wall mate
				5,	# front wall mate
				3,	# right wall mate
				4,	# top wall mate
				1	# bottom wall mate
			]
		self.wallMatesIndexes2 = [				# indexes of cell.wallMates mapped to corresponding surfaces - cell coordinates: z, x, y
				2,	# back wall mate
				1,	# left wall mate
				3,	# front wall mate
				4,	# right wall mate
				5,	# top wall mate
				0	# bottom wall mate
			]
		self.verticiesBigCube = [
			[self.lenBigCube, 0, 0],
			[self.lenBigCube, self.lenBigCube, 0],
			[0, self.lenBigCube, 0],
			[0, 0, 0],
			[self.lenBigCube, 0, self.lenBigCube],
			[self.lenBigCube, self.lenBigCube, self.lenBigCube],
			[0, 0, self.lenBigCube],
			[0, self.lenBigCube, self.lenBigCube]
		]
		cellX = 0; cellY = 0; cellZ = 0; d = 0		
		self.verticiesSmallCube = [
			[(cellX + 1) * d, 	(cellY * d),	 	(cellZ * d)],
			[(cellX + 1) * d, 	(cellY + 1) * d, 	(cellZ * d)],
			[(cellX * d),	 	(cellY + 1) * d, 	(cellZ * d)],
			[(cellX * d),	 	(cellY * d),	 	(cellZ * d)],
			[(cellX + 1) * d, 	(cellY * d),	 	(cellZ + 1) * d],
			[(cellX + 1) * d, 	(cellY + 1) * d, 	(cellZ + 1) * d],
			[(cellX * d),	 	(cellY * d),	 	(cellZ + 1) * d],
			[(cellX * d),	 	(cellY + 1) * d, 	(cellZ + 1) * d]
		]
# long data end

		self.rotation = 00.0						# current rotation
		self.rotatingSpeed = 10.0
		

	def InitGL(self):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		glutInitWindowSize(self.windowWidth, self.windowHeight)
		glutInitWindowPosition(0, 0)
		glutCreateWindow("Simulation Of Hiv Infection")

		glClearColor(0, 0, 0, 1) # set background colour    
		glClearDepth(1.0)                   
		glDepthFunc(GL_LESS)                
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)                

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()                    
											
		gluPerspective(120, float(self.windowWidth)/float(self.windowHeight), 0.1, 100.0)

		glMatrixMode(GL_MODELVIEW)

		self.initCubes()
		self.initCubes2()
		self.initCubes3()

	### --- Creates all cubes vertices --- ###
	def initCubes(self):
		for x in range(self.cellsInAxis):
			xCubes = []
			for y in range(self.cellsInAxis):
				yCubes = []
				for z in range(self.cellsInAxis):
					zCubes = []
					dx = x * self.lenSmallCube
					dy = y * self.lenSmallCube
					dz = z * self.lenSmallCube

					for vert in self.verticesSmallCube:
						zCubes.append([
								vert[0] + dx,
								vert[1] + dy,
								vert[2] + dz
							])
					yCubes.append(zCubes)
				xCubes.append(yCubes)
			self.cubesVertices.append(xCubes)

	### --- Creates all cubes vertices as arrays for glVertexArray --- ###
	def initCubes2(self):
		for x in range(self.cellsInAxis):
			xCubes = []
			for y in range(self.cellsInAxis):
				yCubes = []
				for z in range(self.cellsInAxis):
					zCubes = []
					dx = x * self.lenSmallCube
					dy = y * self.lenSmallCube
					dz = z * self.lenSmallCube

					for vert in self.verticesSmallCube:
						zCubes += [
								vert[0] + dx,
								vert[1] + dy,
								vert[2] + dz
							]
					yCubes.append(array('f', zCubes).tostring())
				xCubes.append(yCubes)
			self.cubesAVertices.append(xCubes)

	### --- Creates all cubes vertices as VBO array --- ###
	def initCubes3(self):
		vertexArray = []
		for x in range(self.cellsInAxis):
			for y in range(self.cellsInAxis):
				for z in range(self.cellsInAxis):
					dx = x * self.lenSmallCube
					dy = y * self.lenSmallCube
					dz = z * self.lenSmallCube
					
					for vert in self.verticesSmallCube:
						vertexArray.append([
								vert[0] + dx,
								vert[1] + dy,
								vert[2] + dz
							])
		
		self.vertexArray = numpyArray(vertexArray, dtype = 'f')
		self.indicesArray = numpyArray(self.surfaces, dtype = int32)

		# needed for displayWorld 7, 9, 10
		self.vertexVbo = vbo.VBO(self.vertexArray, target = GL_ARRAY_BUFFER, usage = GL_STATIC_DRAW)
		self.indicesVbo = vbo.VBO(self.indicesArray, target = GL_ELEMENT_ARRAY_BUFFER, usage = GL_STATIC_DRAW)
		
		# needed for displayWorld8
		# self.vaoId = glGenBuffers(1)
		# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vaoId)
		# glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indicesArray, GL_STATIC_DRAW)
		
		# self.vboId = glGenBuffers(1)
		# glBindBuffer(GL_ARRAY_BUFFER, self.vboId)
		# glBufferData(GL_ARRAY_BUFFER, self.vertexArray, GL_STATIC_DRAW)

	def ReSizeGLScene(self, Width, Height):
		if self.windowHeight == 0:                       
			self.windowHeight = 1

		glViewport(0, 0, self.windowWidth, self.windowHeight)        
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, float(self.windowWidth)/float(self.windowHeight), 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)

	def idle(self):
		self.rotation += self.rotatingSpeed
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.rotation, 0, 1, 0)
		sleep(1)
		# glutPostRedisplay()		# to make it rotate

	def drawSmallCube(self, cellX, cellY, cellZ, state):
		d = self.lenSmallCube

		self.verticiesSmallCube[0] = [(cellX + 1) * d, 	(cellY * d),	 	(cellZ * d)]
		self.verticiesSmallCube[1] = [(cellX + 1) * d, 	(cellY + 1) * d, 	(cellZ * d)],
		self.verticiesSmallCube[2] = [(cellX * d),	 	(cellY + 1) * d, 	(cellZ * d)],
		self.verticiesSmallCube[3] = [(cellX * d),	 	(cellY * d),	 	(cellZ * d)],
		self.verticiesSmallCube[4] = [(cellX + 1) * d, 	(cellY * d),	 	(cellZ + 1) * d],
		self.verticiesSmallCube[5] = [(cellX + 1) * d, 	(cellY + 1) * d, 	(cellZ + 1) * d],
		self.verticiesSmallCube[6] = [(cellX * d),	 	(cellY * d),	 	(cellZ + 1) * d],
		self.verticiesSmallCube[7] = [(cellX * d),	 	(cellY + 1) * d, 	(cellZ + 1) * d]
		
		self.drawCube(self.verticiesSmallCube, self.edges, self.colList[state])
	def drawBigCube(self):
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.rotation, 0, 1, 0)
		
		glBegin(GL_LINES)
		glColor4ubv(self.colBigCube)
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.verticiesBigCube[vertex])
		glEnd()
	def drawCube(self, vertices, edges, color):
		glBegin(GL_QUADS) 	# whole cube
		glColor4ubv(color)
		for surf in self.surfaces:

			for vertex in surf:
				color = self.colList[random.randint(0,3)]
				glVertex3fv(vertices[vertex])
		glEnd()

	def drawBigCube2(self):
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.rotation, 0, 1, 0)
				
		glBegin(GL_LINES)		# cube frames only
		glColor4ubv(self.colBigCube)
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.verticesBigCube[vertex])

		glEnd()
	def drawSmallCube2(self, vertices, color):	# draws whole cube with given vertices and color
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.rotation, 0, 1, 0)

		glBegin(GL_QUADS)		# whole cube
		glColor4ubv(color)
		for surf in self.surfaces:
			for vertex in surf:
				glVertex3fv(vertices[vertex])
		glEnd()
	def drawSmallCube4(self, cell):				# draws only outer walls of cell; uses list of cubes' vertices created with initCubes()
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.rotation, 0, 1, 0)

		glBegin(GL_QUADS)		# whole cube
		glColor4ubv(self.colList[cell.myState])
		for surf, wallMateIndex in zip(self.surfaces, self.wallMatesIndexes):
			if not cell.wallMates[wallMateIndex].myState:  # draw wall only if proper wall mate is healthy
				for vertex in surf:
					glVertex3fv(self.cubesVertices[cell.myX][cell.myY][cell.myZ][vertex])
		glEnd()
	def drawSmallCube5(self, cell):				# draws only outer walls of cell; uses list of cubes' vertices created with initCubes() and wallMatesIndexes2
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.rotation, 0, 1, 0)

		glBegin(GL_QUADS)		# whole cube
		glColor4ubv(self.colList[cell.myState])
		for surf, wallMateIndex in zip(self.surfaces, self.wallMatesIndexes2):
			if not cell.wallMates[wallMateIndex].myState:  # draw wall only if proper wall mate is healthy
				for vertex in surf:
					glVertex3fv(self.cubesVertices[cell.myX][cell.myY][cell.myZ][vertex])
		glEnd()
	def drawSmallCube6(self, cell):				# draws cube using vertexArray; uses list of cubes' vertices arrays created with initCubes2()
		glEnableClientState( GL_COLOR_ARRAY )
		glEnableClientState( GL_VERTEX_ARRAY )
		
		glColorPointer(3, GL_FLOAT, 0, self.colAList[cell.myState])		# floats faster for colors

		glVertexPointer(3, GL_FLOAT, 0, self.cubesAVertices[cell.myX][cell.myY][cell.myZ])			#bytes faster for vertices

		# print(self.cubesAVertices[cell.myX][cell.myY][cell.myZ])

		glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, self.surfacesA)	# whole cube is faster than 6 separate walls
		# for i in range(6):
			# glDrawElements( GL_QUADS, 4, GL_UNSIGNED_BYTE, wallsList[i] )

		glDisableClientState( GL_COLOR_ARRAY )
		glDisableClientState( GL_VERTEX_ARRAY )
	def drawSmallCube7(self, cell):				# draws cube using VBO (not really i think); uses VBO array created with initCubes3()
		beginIndex = cell.myX * self.xCoefficient + cell.myY * self.yCoefficient + cell.myZ * self.zCoefficient

		glEnableClientState( GL_VERTEX_ARRAY )

		glColor4ubv(self.colList[cell.myState])

		glVertexPointer(3, GL_FLOAT, 0, self.vertexVbo + beginIndex)			#bytes faster for vertices
		glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, self.surfacesA)	# whole cube is faster than 6 separate walls
		# glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, self.indicesVbo)	# whole cube is faster than 6 separate walls
		glDisableClientState( GL_VERTEX_ARRAY )
	def drawSmallCube8(self, cell):				# draws cube using VBO; uses VBO array created with initCubes3()
		beginIndex = cell.myX * self.xCoefficient + cell.myY * self.yCoefficient + cell.myZ * self.zCoefficient
		
		glBindBuffer(GL_ARRAY_BUFFER, self.vboId)
		glVertexAttribPointer(self.vboId, 3, GL_FLOAT, GL_FALSE, 0, None)

		# glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vaoId)
		
		# glColor4ubv(self.colList[cell.myState])

		glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, None)	# whole cube is faster than 6 separate walls
	def drawSmallCube9(self, cell):				# draws cube using VBO (not really i think); uses VBO array created with initCubes3(); color should be set in display world
		glEnableClientState( GL_VERTEX_ARRAY )

		# this is faster than glDrawElementsBaseVertex
		beginIndex = cell.myX * self.xCoefficient + cell.myY * self.yCoefficient + cell.myZ * self.zCoefficient
		glVertexPointer(3, GL_FLOAT, 0, self.vertexVbo + beginIndex)			#bytes faster for vertices
		glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, self.surfacesA)	# whole cube is faster than 6 separate walls

		glDisableClientState( GL_VERTEX_ARRAY )
	def drawSmallCube10(self, cell):				# draws cube using VBO (not really i think); uses VBO array created with initCubes3(); color should be set in display world
		beginIndex = cell.myX * self.xCoefficient + cell.myY * self.yCoefficient + cell.myZ * self.zCoefficient

		glEnableClientState( GL_VERTEX_ARRAY )

		glVertexPointer(3, GL_FLOAT, 0, self.vertexVbo + beginIndex)			# bytes faster for vertices

		glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, self.currentSurfacesA)	# whole cube is faster than 6 separate walls

		# glDrawElementsBaseVertex()


		# glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, self.indicesVbo)	# whole cube is faster than 6 separate walls
		glDisableClientState( GL_VERTEX_ARRAY )

	def displayWorld(self):
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait
		
		try:
			# print("starting displaying world")
			displayTime = time()
			
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    

			self.drawBigCube()
			
			for cellsLayer in self.cellsList:
				for cellsRow in cellsLayer:
					for cell in cellsRow:
						if cell.myState != 0:
							self.drawSmallCube(cell.myX, cell.myY, cell.myZ, cell.myState)

			glutSwapBuffers()

			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)

		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
	def displayWorld2(self):			# draw all non-healthy cells
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    

			self.drawBigCube2()
			
			for cellsLayer in self.cellsList:
				for cellsRow in cellsLayer:
					for cell in cellsRow:
						if cell.myState:
							self.drawSmallCube2(self.cubesVertices[cell.myX][cell.myY][cell.myZ], self.colList[cell.myState])

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
	def displayWorld3(self):			# display all cubes from cellsListToDisplay
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    

			self.drawBigCube2()

			for cell in self.cellsListToDisplay:
				self.drawSmallCube2(self.cubesVertices[cell.myX][cell.myY][cell.myZ], self.colList[cell.myState])

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
	def displayWorld4(self):			# display outer walls of cubes from cellsListToDisplay
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    

			self.drawBigCube2()

			for cell in self.cellsListToDisplay:
				self.drawSmallCube4(cell)

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
	def displayWorld5(self):			# draw outer walls of non-healthy and border cells
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    

			self.drawBigCube2()

			for cellsLayer in self.cellsList:
				for cellsRow in cellsLayer:
					for cell in cellsRow:
						if cell.myState:
							l = self.cellsInAxis - 1 	# index of last cell
							if (cell.myX == 0 or cell.myY == 0 or cell.myZ == 0
									or cell.myX == l or cell.myY == l or cell.myZ == l):
								self.drawSmallCube2(self.cubesVertices[cell.myX][cell.myY][cell.myZ], self.colList[cell.myState])
							else:
								self.drawSmallCube5(cell)

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
	def displayWorld6(self):			# draw cubes from cellsListToDisplay using VertexArray
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
			# glMatrixMode( GL_PROJECTION )
			# glLoadIdentity( )
			# glOrtho( -200, 200, -200, 200, -200, 200 )
			# glMatrixMode( GL_MODELVIEW )

			self.drawBigCube2()

			glLoadIdentity()
			glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
			glRotatef(self.rotation, 0, 1, 0)

			for cell in self.cellsListToDisplay:
				if cell.isBorderCell or not all(cell.wallMates):			# if border cell or any neighbour is healthy, print cell
					self.drawSmallCube6(cell)

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
	def displayWorld7(self):			# draw cubes from cellsListToDisplay using VBO (I dont think so)
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
			# glMatrixMode( GL_PROJECTION )
			# glLoadIdentity( )
			# glOrtho( -200, 200, -200, 200, -200, 200 )
			# glMatrixMode( GL_MODELVIEW )

			self.drawBigCube2()

			# self.vbo.bind()
			self.vertexVbo.bind()

			glLoadIdentity()
			glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
			glRotatef(self.rotation, 0, 1, 0)

			for cell in self.cellsListToDisplay:
				if cell.isBorderCell or not all(cell.wallMates):			# if border cell or any neighbour is healthy, print cell
					self.drawSmallCube7(cell)

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
			# self.vbo.unbind()

	def displayWorld8(self):			# draw cubes from cellsListToDisplay using VBO
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
			# glMatrixMode( GL_PROJECTION )
			# glLoadIdentity( )
			# glOrtho( -200, 200, -200, 200, -200, 200 )
			# glMatrixMode( GL_MODELVIEW )

			self.drawBigCube2()

			glLoadIdentity()
			glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
			glRotatef(self.rotation, 0, 1, 0)

			for cell in self.cellsListToDisplay:
				if cell.isBorderCell or not all(cell.wallMates):			# if border cell or any neighbour is healthy, print cell
					self.drawSmallCube8(cell)

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
			# self.vbo.unbind()
	def displayWorld9(self):			# draw cubes from cellsListToDisplay2 using VBO (I dont think so)
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

			self.drawBigCube2()

			self.vertexVbo.bind()

			glLoadIdentity()
			glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
			glRotatef(self.rotation, 0, 1, 0)

			for cellsInOneState in self.cellsListToDisplay2:
				if cellsInOneState:			# check if list not empty
					glColor4ubv(self.colList[cellsInOneState[0].myState])
					for cell in cellsInOneState:
						if cell.isBorderCell or not all(cell.wallMates):			# if border cell or any neighbour is healthy, print cell
							self.drawSmallCube9(cell)

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
			# self.vbo.unbind()
	def displayWorld10(self):			# draw cubes from cellsListToDisplay2 using VBO (I dont think so); displays only visible walls (not always)
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait

		try:
			# print("starting displaying world")
			displayTime = time()

			glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
			# glMatrixMode( GL_PROJECTION )
			# glLoadIdentity( )
			# glOrtho( -200, 200, -200, 200, -200, 200 )
			# glMatrixMode( GL_MODELVIEW )

			self.drawBigCube2()

			self.vertexVbo.bind()

			glLoadIdentity()
			glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
			glRotatef(self.rotation, 0, 1, 0)

			self.distinguishCurrentSurfaces()
			
			for cellsInOneState in self.cellsListToDisplay2:
				if cellsInOneState:			# check if list not empty
					glColor4ubv(self.colList[cellsInOneState[0].myState])

					# glEnableClientState( GL_COLOR_ARRAY )
					# glColorPointer(3, GL_FLOAT, 0, self.colAList[cellsInOneState[0].myState])		# floats faster for colors

					for cell in cellsInOneState:
						if cell.isBorderCell or not all(cell.wallMates):			# if border cell or any neighbour is healthy, print cell
							self.drawSmallCube10(cell)
					
					# glDisableClientState( GL_COLOR_ARRAY )

			glutSwapBuffers()
			displayTime = time() - displayTime
			# print("finished displaying world: ", displayTime)
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
			# self.vbo.unbind()

	def startDisplayingWorld(self):
		self.simSem.acquire()	# take simulation semaphore to initialize itself and display first step
		
		self.InitGL()

		fun = self.displayWorld9
		print('using displaying function:', fun)

		glutDisplayFunc(fun)

		glutIdleFunc(self.idle)
		glutReshapeFunc(self.ReSizeGLScene)
		# glutKeyboardFunc(keyPressed)
		
		glutMainLoop()

	def refreshDisplay(self, cellsListToDisplay, cellsListToDisplay2):
		self.cellsListToDisplay = cellsListToDisplay
		self.cellsListToDisplay2 = cellsListToDisplay2
		glutPostRedisplay()

	def distinguishCurrentSurfaces(self):		# checks which surfaces should be displayed and updates self.currentSurfacesA
		currentAngle = self.rotation % 360.0
		if currentAngle < 90:
			self.currentSurfacesA = self.surfacesFrontLeftA
		elif currentAngle < 180:
			self.currentSurfacesA = self.surfacesBackLeftA
		elif currentAngle < 270:
			self.currentSurfacesA = self.surfacesBackRightA
		else:
			self.currentSurfacesA = self.surfacesFrontRightA
