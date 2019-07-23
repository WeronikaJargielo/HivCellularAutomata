from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from time import sleep

class VisualisationVol2():

	def __init__(self,**kwargs):

		self.windowWidth = 800
		self.windowHeight = 600

		self.maxLenSideCube = 1.5 # half of len of the side of the cube
		self.maxElementsInSingleAxis = kwargs.get('cellsNumberInAxis', -1)
		self.delta = 2 * self.maxLenSideCube / self.maxElementsInSingleAxis

		# self.timeDelay = kwargs.get('simTimeDelay', 500)

		self.colHealthy = (0, 0, 0, 0)
		self.colInfected1 = (255, 255, 0, 255) # yellow
		self.colInfected2 = (255, 155, 0, 255) # orange
		self.colDead = (255, 0, 0, 255) # red
		self.colList = [self.colHealthy, self.colInfected1, self.colInfected2, self.colDead]
		self.colBigCube = (255, 255, 255, 255)
		self.edges = (
					(0,1),
					(0,3),
					(0,4),
					(2,1),
					(2,3),
					(2,7),
					(6,3),
					(6,4),
					(6,7),
					(5,1),
					(5,4),
					(5,7)
					)

		self.verticiesBigCube = (
				(self.maxLenSideCube, -self.maxLenSideCube, -self.maxLenSideCube),
				(self.maxLenSideCube, self.maxLenSideCube, -self.maxLenSideCube),
				(-self.maxLenSideCube, self.maxLenSideCube, -self.maxLenSideCube),
				(-self.maxLenSideCube, -self.maxLenSideCube, -self.maxLenSideCube),
				(self.maxLenSideCube, -self.maxLenSideCube, self.maxLenSideCube),
				(self.maxLenSideCube, self.maxLenSideCube, self.maxLenSideCube),
				(-self.maxLenSideCube, -self.maxLenSideCube, self.maxLenSideCube),
				(-self.maxLenSideCube, self.maxLenSideCube, self.maxLenSideCube)
			)

		cellX = 0; cellY = 0; cellZ = 0; L = 0; d = 0
		self.verticiesSmallCube = [
			[-L + (cellX + 1) * d, 	-L + (cellY * d),	 	-L + (cellZ * d)],
			[-L + (cellX + 1) * d, 	-L + (cellY + 1) * d, 	-L + (cellZ * d)],
			[-L + (cellX * d),	 	-L + (cellY + 1) * d, 	-L + (cellZ * d)],
			[-L + (cellX * d),	 	-L + (cellY * d),	 	-L + (cellZ * d)],
			[-L + (cellX + 1) * d, 	-L + (cellY * d),	 	-L + (cellZ + 1) * d],
			[-L + (cellX + 1) * d, 	-L + (cellY + 1) * d, 	-L + (cellZ + 1) * d],
			[-L + (cellX * d),	 	-L + (cellY * d),	 	-L + (cellZ + 1) * d],
			[-L + (cellX * d),	 	-L + (cellY + 1) * d, 	-L + (cellZ + 1) * d]
		]

		# have no fucking idea what are these
		self.rtri  = 0.0	# rotating speed
		

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
		glPolygonMode(GL_FRONT, GL_LINE)    
		glPolygonMode(GL_BACK, GL_LINE)     
		glShadeModel(GL_SMOOTH)                

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()                    
											
		gluPerspective(120, float(self.windowWidth)/float(self.windowHeight), 0.1, 100.0)

		glMatrixMode(GL_MODELVIEW)


	def ReSizeGLScene(self, Width, Height):
		if self.windowHeight == 0:                       
			self.windowHeight = 1

		glViewport(0, 0, self.windowWidth, self.windowHeight)        
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, float(self.windowWidth)/float(self.windowHeight), 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)


	# def idle(self):
	# 	glLoadIdentity()
	# 	glTranslatef(0.0, 0.0, -4 * self.maxLenSideCube)
	# 	glRotatef(1, 0, 1, 0)
	# 	print("idle working")
	# 	sleep(1)


	def drawSmallCube(self, cellX, cellY, cellZ, state):
		L = self.maxLenSideCube # do skrocenia zapisu
		d = self.delta 

		self.verticiesSmallCube[0] = [-L + (cellX + 1) * d, 	-L + (cellY * d),	 	-L + (cellZ * d)]
		self.verticiesSmallCube[1] = [-L + (cellX + 1) * d, 	-L + (cellY + 1) * d, 	-L + (cellZ * d)],
		self.verticiesSmallCube[2] = [-L + (cellX * d),	 	-L + (cellY + 1) * d, 	-L + (cellZ * d)],
		self.verticiesSmallCube[3] = [-L + (cellX * d),	 	-L + (cellY * d),	 	-L + (cellZ * d)],
		self.verticiesSmallCube[4] = [-L + (cellX + 1) * d, 	-L + (cellY * d),	 	-L + (cellZ + 1) * d],
		self.verticiesSmallCube[5] = [-L + (cellX + 1) * d, 	-L + (cellY + 1) * d, 	-L + (cellZ + 1) * d],
		self.verticiesSmallCube[6] = [-L + (cellX * d),	 	-L + (cellY * d),	 	-L + (cellZ + 1) * d],
		self.verticiesSmallCube[7] = [-L + (cellX * d),	 	-L + (cellY + 1) * d, 	-L + (cellZ + 1) * d]
		
		self.drawCube(self.verticiesSmallCube, self.edges, self.colList[state])


	def drawBigCube(self):
		self.drawCube(self.verticiesBigCube, self.edges, self.colBigCube)


	def drawCube(self, verticies, edges, color):
		glLoadIdentity()
		glTranslatef(0.0, 0.0, -4 * self.maxLenSideCube)
		glRotatef(self.rtri, 0, 1, 0)
		glBegin(GL_LINES)
		
		glColor4ubv(color)
		for edge in edges:
			for vertex in edge:
				glVertex3fv(verticies[vertex])
		glEnd()


	def displayWorld(self, cellsList):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    

		self.drawBigCube()
		
		for cellsLayer in cellsList:
			for cellsRow in cellsLayer:
				for cell in cellsRow:
					if cell.myState != 0:
						self.drawSmallCube(cell.myX, cell.myY, cell.myZ, cell.myState)

		self.rtri  = self.rtri + 2

		glutSwapBuffers()

		print("displaying world")
	
	
	def startDisplayingWorld(self, cellsList):
		displayFuncHandle = lambda : self.displayWorld(cellsList)	# set display function

		self.InitGL()

		glutDisplayFunc(displayFuncHandle)
		# glutIdleFunc(self.idle)
		glutReshapeFunc(self.ReSizeGLScene)
		# glutKeyboardFunc(keyPressed)
		
		glutMainLoop()

	def refreshDisplay(self):
		glutPostRedisplay()
