from classes.World import *
from classes.Cell import *
import OpenGL
import pygame

if __name__ == '__main__':
    myWolrd = World(rows = 3, cols = 3, layers = 3, numberOfIterations = 5)
    myWolrd.printWorld()
    myWolrd.simulateWorld()

    #comment