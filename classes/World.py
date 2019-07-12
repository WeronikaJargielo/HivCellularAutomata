from classes.Cell import *
import random

class World():

    def __init__(self, rows_, cols_, steps_, numberAliveCellsAtStart_):

        self.rows = rows_ # numbers of rows
        self.cols = cols_ # numbers of cols
        
        self.steps = steps_ # numbers of iterations
        self.numberAliveCellsAtStart = numberAliveCellsAtStart_

        self.printChange = False
   
        self.cellsList = []

    def createWorld(self):
        for r in range(self.rows): # loop creating list of cells
            singleRow = []
            for c in range(self.cols):
                cell = Cell(myX=r, myY=c)
                singleRow.append(cell)
            self.cellsList.append(singleRow)
        

        ## setting features of World ##
        self.setParticularStateOfRandomCells(1,self.numberAliveCellsAtStart)
        for upR in range(self.rows): # loop creating list of cells
            for upC in range(self.cols):
                cell = self.cellsList[upR][upC]
                print([upR,upC]) # print #TESTTTTT
                neighboursIndexes = self.getCellNeighbourIndex(cell)
                print(neighboursIndexes) # print ### TESTTTT
                cell.allMates = neighboursIndexes ## !
                print(cell.allMates) ##com
                print(self.getCellNeighbourState(cell))
        
                
    def printWorld(self):
        for i in range(len(self.cellsList)):
            print(self.cellsList[i])

    def setParticularStateOfRandomCells(self, stateValue, numberOfParticularCell): # generating random list of alive cells
        counter = 0
        while counter < numberOfParticularCell:
            tmpXY = [random.randrange(0,self.rows), random.randrange(0,self.cols)]
            setX = tmpXY[0]; setY = tmpXY[1]
            if self.cellsList[setX][setY].myState != stateValue:
                self.cellsList[setX][setY].myState = stateValue
                self.cellsList[setX][setY].newState = stateValue
                counter = counter + 1
            else: 
                pass

    def getCellNeighbourIndex(self,cell): # returns the list of index of cell's neighbours
        cellsMatesIndexes = []
        x = cell.myX # x
        y = cell.myY # y
        allPossibleMates = [[x-1,y-1],[x,y-1],[x+1,y-1],[x-1,y],[x+1,y],[x-1,y+1],[x,y+1],[x+1,y+1]] # all possible mates
        for i in range(len(allPossibleMates)): # checking if the cell is not a norrow one
            try:
                possibleX = allPossibleMates[i][0] # one of possible mates - X
                possibleY = allPossibleMates[i][1] # one of possible mates - Y
                if (possibleX >= 0 and possibleY >= 0):
                    findOutIfMate = self.cellsList[possibleX][possibleY] # try to get out possible mate 
                    myMate = [possibleX,possibleY]
                    cellsMatesIndexes.append(myMate) # append the cellMatesIndex list 
                else:
                    pass
            except IndexError:
                pass # if error appeared, it means that the cell is the norrow one; do nothing
        return cellsMatesIndexes

    def getCellNeighbourState(self,cell): # returns the list of cell's neighbours state
        cellMatesStates = [] # list of states of particular cell
        cellsMatesIndexes = cell.allMates # indexes of cell's neighbour
        for i in range(len(cellsMatesIndexes)):
            tmpX = cellsMatesIndexes[i][0]
            tmpY = cellsMatesIndexes[i][1]
            tmpState = self.cellsList[tmpX][tmpY].myState
            cellMatesStates.append(tmpState)
        return cellMatesStates
           

    def simulateWorld(self): # simulation of world
        for i in range(self.steps):
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.cellsList[r][c]  # single cell
                    cellMatesStates = self.getCellNeighbourState(cell) # get list of neighbours' states of the cell
                    cell.findOutMyState(cellMatesStates) # find out new state of cell 

            for upR in range(self.rows): # loops to update states of all cells at once
                for upC in range(self.cols):
                    cell = self.cellsList[upR][upC]  # single cell
                    cell.state = cell.newState # update cell.state of cell
            print("")
            self.printWorld()
        

    # change the creation of the world


