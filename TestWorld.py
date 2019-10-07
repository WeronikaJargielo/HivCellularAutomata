import unittest
from classes.World import *
from classes.Cell import *

# Comment line below in contractor of class World before running the test
# self.setStateOfIntialI1Cell(self.numberOfI1Cell) # setting the state of I1 cells randomly selected

class TestWorld(unittest.TestCase):

    ### --- settings --- ###
    def setUp(self):
        
        self.myWorld = World(rows = 3, cols = 3, layers = 3, numberOfIterations = 3)

    ## --- findOutCellState method --- ###
    def test_HtoI1StateChangeVar1(self):         # cell.numberOfMatesInSpecificState(cell.wallMates, self.infected1) >= 1 
                                                 # cell.numberOfMatesInSpecificState(cell.lineMates, self.infected1) >= 1 
        cell = self.myWorld.cellsList[1][0][1]
        cell.myState = 1
        for l in range(self.myWorld.layers):
            for r in range(self.myWorld.rows):
                for c in range(self.myWorld.cols):
                    self.myWorld.findOutStateOfCell(self.myWorld.cellsList[l][r][c])

        for c in cell.wallMates:
            self.assertEqual(c.newState, 1) 
        for c in cell.lineMates:
            self.assertEqual(c.newState, 1)
        for c in cell.pointMates:
            self.assertEqual(c.newState, 0)
            
    def test_HtoI1StateChangeVar2(self):    # cell.numberOfMatesInSpecificState(cell.wallMates, self.infected2) >= 5 # I2 cell, wall neighborhood
                                            # cell.numberOfMatesInSpecificState(cell.lineMates, self.infected2) >= 9 # I2 cell, line neighborhood
                                            # cell.numberOfMatesInSpecificState(cell.pointMates, self.infected2) >= 4 # I2 cell, point neighborhood
        cell = self.myWorld.cellsList[1][0][1]
        cell.myState = 0
        

        for w in cell.wallMates:
            w.myState = 2
        for l in cell.lineMates:
            l.myState = 2
        for p in cell.pointMates:
            p.myState = 2
        
        self.myWorld.findOutStateOfCell(cell)
        self.assertEqual(cell.newState, 1)

    def test_I2toDStateChangeVar2(self): # I2 --> dead after two iterations in I2 state (in 3 iteration)
        cell = self.myWorld.cellsList[1][0][1]
        cell.myState = 2
        self.myWorld.simulateWorld()

        self.assertEqual(cell.myState, 3)

if __name__ == '__main__':
    unittest.main()