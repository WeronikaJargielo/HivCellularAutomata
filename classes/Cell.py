class Cell():
    
    def __init__(self,**kwargs): # state, myX, myY, aliveMates, deadMates
       
        self.myState = kwargs.get('state', 0)  # state of the cell
        # kwargs.get('nameOfParametr', defaultValue)
        self.myX = kwargs.get('myX', -1) # cordinates of cell
        self.myY = kwargs.get('myY', -1)  
        self.newState = self.myState
        self.stateChange = False

        i = self.myX
        j = self.myY
        self.allMates = [] # list of list of indexes of all mates  
        self.deadMates = -1 # number of dead neighbours
        self.aliveMates = -1 # number of alive neighbours

        # rules of game
        self.fromDeadToAlive = 3
        self.stayAliveLow = 2
        self.stayAliveHigh = 3 # in other situations cell die 

    def howManyDeadMates(self, listOfCellMatesStates):
        self.deadMates =  listOfCellMatesStates.count(0) # 0 means dead

    def howManyAliveMates(self, listOfCellMatesStates):
        self.aliveMates = listOfCellMatesStates.count(1) # 1 means alive

    def findOutMyState(self, listOfCellMatesStates): # getting an update on the state
        self.howManyAliveMates(listOfCellMatesStates) #  counting how many alive neighbour has
        self.howManyDeadMates(listOfCellMatesStates) #  counting how many dead neighbour has
        if self.myState == 0:
            if self.aliveMates == self.fromDeadToAlive:
                self.newState = 1
                self.stateChange = True
        elif self.myState == 1:
            if (self.aliveMates < self.stayAliveLow or self.aliveMates >  self.stayAliveHigh):
                self.newState = 0
                self.stateChange = True
        else:
            self.stateChange = False

    def __repr__(self):
        return str(self.myState)
    