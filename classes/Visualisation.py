from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

from time import sleep, time
from threading import Semaphore

import random
from array import array

from numpy import array as numpyArray
from numpy import int32, uint32, concatenate, append

class Visualisation():

	def __init__(self,**kwargs):

		self.windowWidth = kwargs.get('windowWidth', 800)	# main window's width
		self.windowHeight = kwargs.get('windowHeight',600)	# main window's height

		self.cellsList = kwargs.get('cellsList', None)					# list of all cells
		self.cellsInAxis = len(self.cellsList)							# number of little cubes in row
		self.lenBigCube = kwargs.get('bigCubeLength', 3)				# length of frame cube
		self.lenSmallCube = self.lenBigCube / self.cellsInAxis			# length of small cubes

		self.cellsListToDisplay = kwargs.get('cellsListToDisplay', None)	# reference to cells to display

		# self.timeDelay = kwargs.get('simTimeDelay', 500)

		self.simSem = kwargs.get('simSem', None)
		self.displaySem = kwargs.get('displaySem', None)

		self.vertexesPerCube = 24 # number of vertexes needed for drawing one cube
		self.indexesPerCube = 8


		self.xCoefficient = self.indexesPerCube * self.cellsInAxis * self.cellsInAxis	# coefficients needed to find proper vertex position in VBO
		self.yCoefficient = self.indexesPerCube * self.cellsInAxis
		self.zCoefficient = self.indexesPerCube
		
		self.vboId = 0

		self.translateOnX = +self.lenBigCube/4
		self.translateOnY = -self.lenBigCube/2
		self.translateOnZ = -3 * self.lenBigCube

		self.currentRotation = 300.0
		self.rotatingSpeed = 00.0

		self.colBigCube = (255, 255, 255, 255)	# frame cube color - white, opaque

# array colors
		self.colAInf1 = [ [0.6, 0.6, 0],  	[0.9, 0.9, 0],  [0.9, 0.9, 0], [0.8, 0.8, 0], [0.8, 0.8, 0],  [1, 1, 0],  [0.95, 0.95, 0], [1, 1, 0]]	# arrays with cube colors
		self.colAInf2 = [ [0.6, 0.3, 0], 	[0.9, 0.5, 0],[0.9, 0.5, 0], [0.8, 0.4, 0], [0.8, 0.4, 0], [1, 0.6, 0], [0.95, 0.55, 0], [1, 0.6, 0]]
		self.colADead = [ [0.6, 0, 0],  	[0.9, 0, 0],  [0.9, 0, 0],   [0.8, 0, 0],  [0.8, 0, 0],  [1, 0, 0],  [0.95, 0, 0],  [1, 0, 0]]
		self.colAList = [self.colAInf1, self.colAInf2, self.colADead] # enables setColor(self.colAList[cell.state - 1])

# array vertices
		self.surfacesA = array('B', [						# vertices numbers for all surfaces 
				0,1,2,3,	# back wall
				3,2,7,6,	# left wall
				6,7,5,4,	# front wall
				4,5,1,0,	# right wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			]).tostring()

# long data
		self.bigCubeEdgesIndexes = array('B', [0,1, 0,3, 0,4, 2,1, 2,3, 2,7, 6,3, 6,4, 6,7, 5,1, 5,4, 5,7]).tobytes()
		self.numberOfEdgesIndexes = 24
		self.verticesBigCubeA = array('f',[				# big cube vertices
				self.lenBigCube, 	0, 					0,
				self.lenBigCube, 	self.lenBigCube, 	0,
				0, 				self.lenBigCube, 	0,
				0, 				0, 					0,
				self.lenBigCube, 	0, 					self.lenBigCube,
				self.lenBigCube, 	self.lenBigCube, 	self.lenBigCube,
				0, 				0, 					self.lenBigCube,
				0, 				self.lenBigCube, 	self.lenBigCube
			]).tobytes()
# long data end

		self.byteStrideBetweenVertexes = 24
		
		

	def InitGL(self):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		glutInitWindowSize(self.windowWidth, self.windowHeight)
		glutInitWindowPosition(100, 100)
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

	### --- Creates all cubes vertices as VBO array --- ###
	def initCubes(self):
		verticesSmallCube = [				# small cubes vertices
				[self.lenSmallCube, 0, 					0],
				[self.lenSmallCube, self.lenSmallCube, 	0],
				[0, 				self.lenSmallCube, 	0],
				[0, 				0, 					0],
				[self.lenSmallCube, 0, 					self.lenSmallCube],
				[self.lenSmallCube, self.lenSmallCube, 	self.lenSmallCube],
				[0, 				0, 					self.lenSmallCube],
				[0, 				self.lenSmallCube, 	self.lenSmallCube]
			]
		vertexArray = []
		vertexArrayInf1 = []
		vertexArrayInf2 = []
		vertexArrayDead = []
		self.cellsIndexes = []
		for x in range(self.cellsInAxis):
			xIndexes = []
			for y in range(self.cellsInAxis):
				yIndexes = []
				for z in range(self.cellsInAxis):
					dx = x * self.lenSmallCube
					dy = y * self.lenSmallCube
					dz = z * self.lenSmallCube
					
					for vert in verticesSmallCube:
						vertexArray.append([vert[0] + dx, vert[1] + dy, vert[2] + dz])
					
					for vert, color in zip(verticesSmallCube, self.colAInf1):
						vertexArrayInf1.append([vert[0] + dx, vert[1] + dy, vert[2] + dz])
						vertexArrayInf1.append(color)
					for vert, color in zip(verticesSmallCube, self.colAInf2):
						vertexArrayInf2.append([vert[0] + dx, vert[1] + dy, vert[2] + dz])
						vertexArrayInf2.append(color)
					for vert, color in zip(verticesSmallCube, self.colADead):
						vertexArrayDead.append([vert[0] + dx, vert[1] + dy, vert[2] + dz])
						vertexArrayDead.append(color)

					yIndexes.append(self.initSurfaces(x, y, z))	# needed by 12
				xIndexes.append(yIndexes)
			self.cellsIndexes.append(xIndexes)		
		
		# vertexArray = numpyArray(vertexArray, dtype = 'f')
		vertexArrayInf1 = numpyArray(vertexArrayInf1, dtype = 'f')
		vertexArrayInf2 = numpyArray(vertexArrayInf2, dtype = 'f')
		vertexArrayDead = numpyArray(vertexArrayDead, dtype = 'f')

		# self.vertexVbo = vbo.VBO(vertexArray, target = GL_ARRAY_BUFFER, usage = GL_STATIC_DRAW)
		self.vertexVboInf1 = vbo.VBO(vertexArrayInf1, target = GL_ARRAY_BUFFER, usage = GL_STATIC_DRAW)
		self.vertexVboInf2 = vbo.VBO(vertexArrayInf2, target = GL_ARRAY_BUFFER, usage = GL_STATIC_DRAW)
		self.vertexVboDead = vbo.VBO(vertexArrayDead, target = GL_ARRAY_BUFFER, usage = GL_STATIC_DRAW)
		
		self.vertexVbos = [self.vertexVboInf1, self.vertexVboInf2, self.vertexVboDead]

		# self.vboId = glGenBuffers(1)
		# glBindBuffer(GL_ARRAY_BUFFER, self.vboId)
		# glBufferData(GL_ARRAY_BUFFER, self.vertexArray, GL_STATIC_DRAW)

	def initSurfaces(self, x, y, z):
		beginIndex = x * self.xCoefficient + y * self.yCoefficient + z * self.zCoefficient
		surfaces = array('I', [						# vertices numbers for all surfaces 
				0,1,2,3,	# hontho wall
				3,2,7,6,	# left wall
				6,7,5,4,	# front wall
				4,5,1,0,	# right wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			])
		# surfaces = numpyArray([						# vertices numbers for all surfaces 
		# 		0,1,2,3,	# back wall
		# 		3,2,7,6,	# left wall
		# 		6,7,5,4,	# front wall
		# 		4,5,1,0,	# right wall
		# 		1,5,7,2,	# top wall
		# 		4,0,3,6		# bottom wall
		# 	], dtype=uint32)
		for i in range(len(surfaces)):
			surfaces[i] += beginIndex
		return surfaces

	def ReSizeGLScene(self, Width, Height):
		if self.windowHeight == 0:                       
			self.windowHeight = 1

		glViewport(0, 0, self.windowWidth, self.windowHeight)        
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, float(self.windowWidth)/float(self.windowHeight), 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)

	def idle(self):
		self.currentRotation += self.rotatingSpeed
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.currentRotation, 0, 1, 0)
		sleep(1)
		glutPostRedisplay()		# to make it rotate

	def drawBigCube(self):
		glLoadIdentity()
		glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
		glRotatef(self.currentRotation, 0, 1, 0)

		glColor4ubv(self.colBigCube)

		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3, GL_FLOAT, 0, self.verticesBigCubeA)
		glDrawElements(GL_LINES, self.numberOfEdgesIndexes, GL_UNSIGNED_BYTE, self.bigCubeEdgesIndexes)
		glDisableClientState(GL_VERTEX_ARRAY)

	# draws cubes using VBO
	def drawSmallCubes(self, indexesToDisplay, currentVertexVbo):
		
		
		glEnableClientState(GL_COLOR_ARRAY)
		glColorPointer(3, GL_FLOAT, self.byteStrideBetweenVertexes, currentVertexVbo + int(self.byteStrideBetweenVertexes/2))

		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3, GL_FLOAT, self.byteStrideBetweenVertexes, currentVertexVbo)				# bytes faster for vertices
		
		glDrawElements(GL_QUADS, len(indexesToDisplay), GL_UNSIGNED_INT, indexesToDisplay.tobytes())	# whole cube is faster than 6 separate walls
		
		glDisableClientState(GL_COLOR_ARRAY)
		glDisableClientState(GL_VERTEX_ARRAY)

	def displayWorld(self):			# draw all 
		self.displaySem.acquire() # take semaphore to display world, so simulation will have to wait
		try:
			displayTime = time()

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

			self.drawBigCube()

			glLoadIdentity()
			glTranslatef(self.translateOnX, self.translateOnY, self.translateOnZ)
			glRotatef(self.currentRotation, 0, 1, 0)

			for cellsInOneState, currentVertexVbo in zip(self.cellsListToDisplay, self.vertexVbos):
				if cellsInOneState:			# check if list not empty
					glColor4ubv(self.colBigCube)

					indexesToDisplay = array('I', [])
					# indexesToDisplay = numpyArray([], uint32)
					for cell in cellsInOneState:
						if cell.isBorderCell or not all(cell.wallMates):			# if border cell or any neighbour is healthy, print cell
							indexesToDisplay.extend(self.cellsIndexes[cell.myX][cell.myY][cell.myZ])	# normal array
							# concatenate((indexesToDisplay, self.cellsIndexes[cell.myX][cell.myY][cell.myZ]))	# numpy array
							# indexesToDisplay = append(indexesToDisplay, self.cellsIndexes[cell.myX][cell.myY][cell.myZ])
					
					currentVertexVbo.bind()
					self.drawSmallCubes(indexesToDisplay, currentVertexVbo)
					currentVertexVbo.unbind()

			glutSwapBuffers()
			displayTime = time() - displayTime
			print("display time: ", displayTime)
	
		finally:
			self.simSem.release()	# end of displaying world, release semaphore for simulation
			pass

	def startDisplayingWorld(self):
		self.simSem.acquire()	# take simulation semaphore to initialize itself and display first step
		
		self.InitGL()

		fun = self.displayWorld
		print('using displaying function:', fun)

		glutDisplayFunc(fun)

		glutIdleFunc(self.idle)
		glutReshapeFunc(self.ReSizeGLScene)
		
		glutMainLoop()

	def refreshDisplay(self, cellsListToDisplay):
		self.cellsListToDisplay = cellsListToDisplay
		glutPostRedisplay()
