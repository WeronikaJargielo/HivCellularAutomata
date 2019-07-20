import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Visualisation():

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


	def init(self):
		pygame.init()
		display = (self.windowWidth, self.windowHeight)
		pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
		gluPerspective(60, (display[0]/display[1]), 0.1, 50.0)
		glTranslatef(0.0, 0.0, -5)


	def drawSmallCube(self, cellX, cellY, cellZ, state):
		L = self.maxLenSideCube # do skrocenia zapisu
		d = self.delta 

		verticies = [
			[-L + (cellX + 1) * d, 	-L + (cellY * d),	 	-L + (cellZ * d)],
			[-L + (cellX + 1) * d, 	-L + (cellY + 1) * d, 	-L + (cellZ * d)],
			[-L + (cellX * d),	 	-L + (cellY + 1) * d, 	-L + (cellZ * d)],
			[-L + (cellX * d),	 	-L + (cellY * d),	 	-L + (cellZ * d)],
			[-L + (cellX + 1) * d, 	-L + (cellY * d),	 	-L + (cellZ + 1) * d],
			[-L + (cellX + 1) * d, 	-L + (cellY + 1) * d, 	-L + (cellZ + 1) * d],
			[-L + (cellX * d),	 	-L + (cellY * d),	 	-L + (cellZ + 1) * d],
			[-L + (cellX * d),	 	-L + (cellY + 1) * d, 	-L + (cellZ + 1) * d]
		]
		
		self.drawCube(verticies, self.edges, self.colList[state])


	def drawBigCube(self):
		self.drawCube(self.verticiesBigCube, self.edges, self.colBigCube)


	def drawCube(self, verticies, edges, color):
		glBegin(GL_LINES)
		glColor4ubv(color) 
		for edge in edges:
			for vertex in edge:
				glVertex3fv(verticies[vertex])
		glEnd()

	

	def displayWorld(self, cellsList):
		glRotatef(1, 0, 1, 0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		self.drawBigCube()

		for cellsLayer in cellsList:
			for cellsRow in cellsLayer:
				for cell in cellsRow:
					self.drawSmallCube(cell.myX, cell.myY, cell.myZ, cell.myState)

		pygame.display.flip()
		pygame.time.wait(10)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.close()
				quit()
	
	def close(self):
		pygame.quit()