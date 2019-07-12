from classes.World import *
from classes.Cell import *

if __name__ == '__main__':
    myWolrd = World(3,3,1,4)
    myWolrd.createWorld()
    myWolrd.printWorld()
    myWolrd.simulateWorld()

    #comment