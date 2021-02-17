from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

from time import sleep, time
from threading import Semaphore

from array import array

from numpy import array as numpyArray
from numpy import uint32

class Visualisation():

	def __init__(self,**kwargs):

		self.windowWidth = kwargs.get('windowWidth', 800)	# main window's width
		self.windowHeight = kwargs.get('windowHeight',450)	# main window's height

		
		self.cellsInAxis = kwargs.get('cellsInAxis', None)
		self.lenBigCube = kwargs.get('bigCubeLength', 3)
		self.lenSmallCube = self.lenBigCube / self.cellsInAxis

		self.cellsListToDisplay = kwargs.get('cellsListToDisplay', None)	# reference to cells to display

		self.simulationSemaphore = kwargs.get('simulationSemaphore', None)
		self.displaySemaphore = kwargs.get('displaySemaphore', None)

		self.numberOfVertexesPerCube = 8

		self.xCoefficient = self.numberOfVertexesPerCube * self.cellsInAxis * self.cellsInAxis	# coefficients needed to find proper vertex position in VBO
		self.yCoefficient = self.numberOfVertexesPerCube * self.cellsInAxis
		self.zCoefficient = self.numberOfVertexesPerCube
		
		self.xTranslation = +self.lenBigCube/8
		self.yTranslation = -self.lenBigCube/2
		self.zTranslation = -3 * self.lenBigCube

		self.currentRotation = 300.0
		self.rotatingSpeed = 00.0

		self.colBigCube = [0, 0, 0]

		self.colAInf1 = [ [0.6, 0.6, 0], [0.9, 0.9, 0],  [0.9, 0.9, 0], [0.8, 0.8, 0], [0.8, 0.8, 0],  [1, 1, 0],  [0.95, 0.95, 0], [1, 1, 0]]
		self.colAInf2 = [ [0.6, 0.3, 0], [0.9, 0.5, 0],[0.9, 0.5, 0], [0.8, 0.4, 0], [0.8, 0.4, 0], [1, 0.6, 0], [0.95, 0.55, 0], [1, 0.6, 0]]
		self.colADead = [ [0.6, 0, 0],   [0.9, 0, 0],  [0.9, 0, 0],   [0.8, 0, 0],  [0.8, 0, 0],  [1, 0, 0],  [0.95, 0, 0],  [1, 0, 0]]
		self.colAList = [self.colAInf1, self.colAInf2, self.colADead] # enables setColor(self.colAList[cell.state - 1])

		self.bigCubeEdgesIndexes = array('B', [0,1, 0,3, 0,4, 2,1, 2,3, 2,7, 6,3, 6,4, 6,7, 5,1, 5,4, 5,7]).tobytes()
		self.numberOfEdgesVertexes = 24
		self.byteStrideBetweenVertexes = 24

		self.verticesBigCubeA = array('f',[				# big cube vertices
				self.lenBigCube, 	0, 					0,
				self.lenBigCube, 	self.lenBigCube, 	0,
				0, 					self.lenBigCube, 	0,
				0, 					0, 					0,
				self.lenBigCube, 	0, 					self.lenBigCube,
				self.lenBigCube, 	self.lenBigCube, 	self.lenBigCube,
				0, 					0, 					self.lenBigCube,
				0, 					self.lenBigCube, 	self.lenBigCube
			]).tobytes()

		self.cellsSurfacesIndexes = None
		self.vertexVbos = None

	def InitGL(self):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		glutInitWindowSize(self.windowWidth, self.windowHeight)
		glutInitWindowPosition(100, 100)
		glutCreateWindow("Simulation Of Hiv Infection")

		glClearColor(255, 255, 255, 1) # set background colour    
		glClearDepth(1.0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
											
		gluPerspective(45, float(self.windowWidth)/float(self.windowHeight), 0.1, 100.0)

		glMatrixMode(GL_MODELVIEW)

		self.initCubes()

	### --- Creates all cubes vertices as VBO arrays --- ###
	def initCubes(self):
		self.cellsSurfacesIndexes = self.initCellsSurfaces()

		self.vertexVbos = self.initVbos()

	def initVbos(self):
		vertexVbos = []
		for colors in self.colAList:
			vertexVbos.append(self.initVertexVboWithColor(colors))
		return vertexVbos

	def initVertexVboWithColor(self, vertexesColors):
		l = self.lenBigCube / self.cellsInAxis # length of small cube
		verticesSmallCube = [ [l, 0, 0], [l, l, 0], [0, l, 0], [0, 0, 0], [l, 0, l], [l, l, l], [0, 0, l], [0, l, l] ]
		vertexArray = []
		for x in range(self.cellsInAxis):
			for y in range(self.cellsInAxis):
				for z in range(self.cellsInAxis):
					dx = x * self.lenSmallCube
					dy = y * self.lenSmallCube
					dz = z * self.lenSmallCube
					
					for vertex, color in zip(verticesSmallCube, vertexesColors):
						vertexArray.append([vertex[0] + dx, vertex[1] + dy, vertex[2] + dz])
						vertexArray.append(color)

		return vbo.VBO(numpyArray(vertexArray, dtype = 'f'), target = GL_ARRAY_BUFFER, usage = GL_STATIC_DRAW)

	def initCellsSurfaces(self):
		cellsSurfacesIndexes = []
		for x in range(self.cellsInAxis):
			yCellsSurfaces = []
			for y in range(self.cellsInAxis):
				zCellsSurfaces = []
				for z in range(self.cellsInAxis):
					zCellsSurfaces.append(self.createSurfacesForCell(x, y, z))
				
				yCellsSurfaces.append(zCellsSurfaces)
			
			cellsSurfacesIndexes.append(yCellsSurfaces)
		
		return cellsSurfacesIndexes

	def createSurfacesForCell(self, x, y, z):
		surfaces = array('I', [						# vertices numbers for all surfaces 
				0,1,2,3,	# back wall
				3,2,7,6,	# left wall
				6,7,5,4,	# front wall
				4,5,1,0,	# right wall
				1,5,7,2,	# top wall
				4,0,3,6		# bottom wall
			])
		beginIndex = x * self.xCoefficient + y * self.yCoefficient + z * self.zCoefficient
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
		sleep(1)

	
	def displayWorld(self):			# draw all 
		self.displaySemaphore.acquire() # take semaphore to display world, so simulation will have to wait
		try:
			displayTime = time()

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

			self.drawBigCube()

			glLoadIdentity()
			glTranslatef(self.xTranslation, self.yTranslation, self.zTranslation)
			glRotatef(self.currentRotation, 0, 1, 0)

			for cellsInOneState, currentVertexVbo in zip(self.cellsListToDisplay, self.vertexVbos):
				if cellsInOneState:			# check if list not empty

					indexesToDisplay = array('I', [])
					for cell in cellsInOneState:
						if cell.isBorderCell or not all(cell.wallMates):			# if border cell or any neighbour is healthy, print cell
							indexesToDisplay.extend(self.cellsSurfacesIndexes[cell.myX][cell.myY][cell.myZ])
					
					currentVertexVbo.bind()
					self.drawSmallCubes(indexesToDisplay, currentVertexVbo)
					currentVertexVbo.unbind()

			glutSwapBuffers()
			displayTime = time() - displayTime
			print("display time: ", displayTime)
	
		finally:
			self.simulationSemaphore.release()	# end of displaying world, release semaphore for simulation

	def drawBigCube(self):
		glLoadIdentity()
		glTranslatef(self.xTranslation, self.yTranslation, self.zTranslation)
		glRotatef(self.currentRotation, 0, 1, 0)

		glColor3ubv(self.colBigCube)

		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3, GL_FLOAT, 0, self.verticesBigCubeA)
		glDrawElements(GL_LINES, self.numberOfEdgesVertexes, GL_UNSIGNED_BYTE, self.bigCubeEdgesIndexes)
		glDisableClientState(GL_VERTEX_ARRAY)

	### --- draws cubes using VBO --- ###
	def drawSmallCubes(self, indexesToDisplay, currentVertexVbo):
		glEnableClientState(GL_COLOR_ARRAY)
		glColorPointer(3, GL_FLOAT, self.byteStrideBetweenVertexes, currentVertexVbo + int(self.byteStrideBetweenVertexes/2))

		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3, GL_FLOAT, self.byteStrideBetweenVertexes, currentVertexVbo)				# bytes faster for vertices
		
		glDrawElements(GL_QUADS, len(indexesToDisplay), GL_UNSIGNED_INT, indexesToDisplay.tobytes())	# whole cube is faster than 6 separate walls
		
		glDisableClientState(GL_COLOR_ARRAY)
		glDisableClientState(GL_VERTEX_ARRAY)

	def startDisplayingWorld(self):
		self.simulationSemaphore.acquire()	# take simulation semaphore to initialize itself and display first step
		
		self.InitGL()

		glutDisplayFunc(self.displayWorld)
		glutIdleFunc(self.idle)
		# glutReshapeFunc(self.ReSizeGLScene)
		
		glutMainLoop()

	def refreshDisplay(self, cellsListToDisplay):
		self.cellsListToDisplay = cellsListToDisplay
		glutPostRedisplay()
